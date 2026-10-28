import matplotlib
matplotlib.use("Agg")

import os
import time
import threading
import tempfile
import traceback
from gom import GoM, ProcessingConfig
from pathlib import Path

from ultralytics import YOLO

# Load environment variables (API token, detection backend) from GESTALT/.env.
# This file lives at GESTALT/image_search_feature/sample.py, so the repo root is
# two levels up. We load it once at import; missing .env is non-fatal.
try:
    from dotenv import load_dotenv
    _ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(_ENV_PATH)
except Exception as _env_exc:  # pragma: no cover - defensive only
    print(f"[IMAGE_DEBUG] could not load .env: {_env_exc!r}")

# --- YOLO-World (open-vocabulary) detection for GoM ---------------------------
#
# GoM's default detector is a closed-vocabulary YOLOv8 trained on COCO. Its
# labels (person, car, ...) are not part of GESTALT's region vocab, so every
# detection gets dropped by prune_invalid_objects before it reaches the canvas.
#
# We swap in a YOLO-World model and prime it with GESTALT's DC vocab via
# set_classes(). YOLO-World is open-vocabulary: set_classes() encodes the given
# phrases with CLIP and the model then only predicts those classes. We feed the
# model into GoM through its detect_fn hook, so GoM skips loading its own YOLO
# and uses our detector for the detection stage (segmentation/depth/relations
# are unchanged).

# Hard-coded DC vocabulary (canonical labels, matching GESTALT's inverted index).
DC_VOCAB_CLASSES = [
    "advertising",
    "anchor",
    "block",
    "bollard",
    "boundary_stone",
    "buffer_stop",
    "bump_gate",
    "bus_stop",
    "bust",
    "cannon",
    "chain",
    "communications_dish",
    "crane",
    "crossing",
    "district",
    "elevator",
    "entrance",
    "firepit",
    "fitness_centre",
    "flagpole",
    "full-height_turnstile",
    "garden",
    "gate",
    "give_way",
    "installation",
    "jersey_barrier",
    "junction",
    "kerb",
    "level_crossing",
    "lift_gate",
    "manhole",
    "maritime",
    "memorial",
    "milestone",
    "mini_roundabout",
    "monitoring_station",
    "monument",
    "mosaic",
    "motorway_junction",
    "ornamental_vase",
    "outdoor_seating",
    "outlet",
    "park",
    "picnic_table",
    "planter",
    "pole",
    "rope",
    "sculpture",
    "sculpture_group",
    "shrub",
    "signal",
    "silo",
    "site",
    "sound installation",
    "speed_display",
    "station",
    "statue",
    "stone",
    "stop",
    "street_lamp",
    "subway_entrance",
    "surveillance",
    "survey_point",
    "swing_gate",
    "switch",
    "table",
    "tomb",
    "tower",
    "traffic_signals",
    "tram_crossing",
    "tram_level_crossing",
    "tram_stop",
    "tree",
    "utility_pole",
    "ventilation_shaft",
    "water_well",
    "wedge",
    "yes",
]

# Natural-language prompts fed to YOLO-World's CLIP text encoder. The canonical
# vocab uses underscores; CLIP works better on plain phrases, so we strip them
# for the prompt while keeping DC_VOCAB_CLASSES as the labels we hand back.
_DC_PROMPTS = [c.replace("_", " ") for c in DC_VOCAB_CLASSES]

# YOLO-World weights live next to the Django project.
_YOLO_WORLD_WEIGHTS = (
    Path(__file__).resolve().parent.parent
    / "scratch" / "drag_and_drop" / "yolov8x-worldv2.pt"
)

# Detection tuning (mirrors the YOLO-World usage example).
_DETECT_CONF = 0.15
_DETECT_IMGSZ = 1280

# The model is heavy to load and is shared across requests, so cache it and
# serialize access (Django's dev server can serve requests on multiple threads).
_yolo_world_model = None
_model_lock = threading.Lock()


def _get_yolo_world_model():
    global _yolo_world_model
    if _yolo_world_model is None:
        with _model_lock:
            if _yolo_world_model is None:
                print(f"[IMAGE_DEBUG] loading YOLO-World weights from {_YOLO_WORLD_WEIGHTS}")
                load_start = time.time()
                model = YOLO(str(_YOLO_WORLD_WEIGHTS))
                model.set_classes(_DC_PROMPTS)
                _yolo_world_model = model
                print(f"[IMAGE_DEBUG] YOLO-World loaded in {time.time() - load_start:.2f}s "
                      f"with {len(_DC_PROMPTS)} DC classes")
    return _yolo_world_model


def make_dc_detect_fn(device=None, conf=_DETECT_CONF, imgsz=_DETECT_IMGSZ):
    """Build a GoM-compatible detect_fn backed by YOLO-World primed on DC vocab.

    GoM calls detect_fn(image: PIL.Image) and expects (boxes, labels, scores)
    where boxes are [x1, y1, x2, y2] in pixels. We map each prediction's class
    index back to the canonical DC_VOCAB_CLASSES label so downstream pruning
    matches GESTALT's vocab exactly.
    """
    model = _get_yolo_world_model()

    def detect_fn(image):
        predict_kwargs = {"conf": conf, "imgsz": imgsz, "verbose": False}
        if device:
            predict_kwargs["device"] = device

        with _model_lock:
            results = model.predict(image, **predict_kwargs)[0]

        boxes, labels, scores = [], [], []
        for box in results.boxes:
            cls_idx = int(box.cls[0])
            boxes.append(box.xyxy[0].tolist())
            labels.append(DC_VOCAB_CLASSES[cls_idx])
            scores.append(float(box.conf[0]))

        print(f"[IMAGE_DEBUG] detect_fn: {len(boxes)} DC detections "
              f"(conf>={conf}) labels={labels}")
        return boxes, labels, scores

    return detect_fn


# --- Grounding DINO 1.5 Pro (DeepDataSpace cloud API) detection for GoM -------
#
# Grounding DINO 1.5 Pro runs through DeepDataSpace's cloud, not local weights.
# NOTE: the original IDEA `gdino` wrapper + dds-cloudapi-sdk 0.2.1 target the
# decommissioned `api.deepdataspace.com/tasks/detection` endpoint (returns
# "Resource Not Found"). We instead call the current V2 API directly via
# dds-cloudapi-sdk >= 0.5 (`/v2/task/grounding_dino/detection`).
#
# Like the YOLO-World path, we expose this to GoM as a detect_fn returning
# (boxes, labels, scores), and map the model's phrase categories back to the
# canonical DC_VOCAB_CLASSES labels so downstream pruning matches GESTALT vocab.

# Grounding DINO expects natural-language phrases separated by ".",
# e.g. "street lamp.bus stop.tree".
def _normalize_for_prompt(label):
    return label.replace("_", " ").replace("-", " ").strip().lower()


_GDINO_PROMPT_TEXT = ".".join(_normalize_for_prompt(c) for c in DC_VOCAB_CLASSES)

# Reverse map: normalized phrase -> canonical DC label, so a returned category
# like "street lamp" resolves back to "street_lamp".
_GDINO_PHRASE_TO_CANONICAL = {
    _normalize_for_prompt(c): c for c in DC_VOCAB_CLASSES
}

_GDINO_MODEL = os.getenv("GDINO_MODEL", "GroundingDino-1.5-Pro")
_GDINO_API_PATH = "/v2/task/grounding_dino/detection"
_GDINO_BBOX_THRESHOLD = float(os.getenv("GDINO_BBOX_THRESHOLD", "0.25"))
_GDINO_IOU_THRESHOLD = float(os.getenv("GDINO_IOU_THRESHOLD", "0.8"))
_GDINO_REQUEST_TIMEOUT = int(os.getenv("GDINO_REQUEST_TIMEOUT", "60"))

# The DeepDataSpace client is created once (token from env) and reused.
_gdino_client = None
_gdino_client_lock = threading.Lock()


def _get_gdino_client():
    global _gdino_client
    if _gdino_client is None:
        with _gdino_client_lock:
            if _gdino_client is None:
                token = os.getenv("DEEPDATASPACE_API_TOKEN")
                if not token:
                    raise RuntimeError(
                        "Missing DEEPDATASPACE_API_TOKEN. Add it to GESTALT/.env "
                        "to use the grounding_dino_15_pro detection backend."
                    )
                from dds_cloudapi_sdk import Config, Client
                print("[IMAGE_DEBUG] initializing DeepDataSpace client for Grounding DINO")
                _gdino_client = Client(Config(token))
    return _gdino_client


def _resolve_gdino_category(category):
    """Map a Grounding DINO phrase category back to a canonical DC label."""
    normalized = _normalize_for_prompt(category)
    if normalized in _GDINO_PHRASE_TO_CANONICAL:
        return _GDINO_PHRASE_TO_CANONICAL[normalized]
    # Grounding DINO can return compound phrases; try a contained-phrase match
    # before giving up (downstream pruning is the final safety net).
    for phrase, canonical in _GDINO_PHRASE_TO_CANONICAL.items():
        if phrase in normalized or normalized in phrase:
            return canonical
    return category


def make_grounding_dino_detect_fn(
    conf=_GDINO_BBOX_THRESHOLD,
    iou=_GDINO_IOU_THRESHOLD,
    model=_GDINO_MODEL,
):
    """Build a GoM-compatible detect_fn backed by Grounding DINO 1.5 Pro (cloud).

    GoM calls detect_fn(image: PIL.Image) and expects (boxes, labels, scores)
    with boxes as [x1, y1, x2, y2] in pixels. We persist the PIL image to a temp
    file, send it to the DeepDataSpace V2 API with the full DC-vocab prompt, and
    convert returned objects back into GoM's format.
    """
    client = _get_gdino_client()
    from dds_cloudapi_sdk.tasks.v2_task import create_task_with_local_image_auto_resize

    def detect_fn(image):
        # GoM hands us a PIL image; the API needs a file (auto-resized + base64).
        # auto-resize sends a smaller image but rescales boxes back to original.
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            image.convert("RGB").save(tmp_path)

            api_body = {
                "model": model,
                "prompt": {"type": "text", "text": _GDINO_PROMPT_TEXT},
                "targets": ["bbox"],
                "bbox_threshold": conf,
                "iou_threshold": iou,
            }
            task = create_task_with_local_image_auto_resize(
                api_path=_GDINO_API_PATH,
                api_body_without_image=api_body,
                image_path=tmp_path,
            )
            task.set_request_timeout(_GDINO_REQUEST_TIMEOUT)
            client.run_task(task)

            objects = (task.result or {}).get("objects", [])
            boxes, labels, scores = [], [], []
            for obj in objects:
                bbox = obj.get("bbox")
                if not bbox:
                    continue
                boxes.append([float(v) for v in bbox])
                labels.append(_resolve_gdino_category(obj.get("category", "")))
                scores.append(float(obj.get("score", 0.0)))

            print(f"[IMAGE_DEBUG] grounding_dino detect_fn: {len(boxes)} detections "
                  f"(model={model}, conf>={conf}) labels={labels}")
            return boxes, labels, scores
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

    return detect_fn


def get_detection_backend():
    """Return the configured detection backend name (defaults to YOLO-World)."""
    return os.getenv("DETECTION_BACKEND", "yolo_world").strip().lower()


def make_detect_fn(device="cpu"):
    """Build the detect_fn for the configured DETECTION_BACKEND."""
    backend = get_detection_backend()
    if backend in ("grounding_dino_15_pro", "grounding_dino", "gdino"):
        print("[IMAGE_DEBUG] detection backend = grounding_dino_15_pro")
        return make_grounding_dino_detect_fn()
    print("[IMAGE_DEBUG] detection backend = yolo_world")
    return make_dc_detect_fn(device=device)


# These two methods are not used anymore, but I will keep them here for reference
# It assumes GoM already ran and gave you a result dictionary r with label and relationship information.
# Then it turns that structured GoM output into plain English text for the LLM.it turns that structured GoM output into plain English text for the LLM.
# So this method does not analyze the image. It only converts GoM results into LLM-readable text.

# def gom_to_llm_text(r):
#     print("[IMAGE_DEBUG] gom_to_llm_text: starting")
#     labels = r["labels"]
#     relationships = r["relationships"]
#     print(f"[IMAGE_DEBUG] gom_to_llm_text: {len(labels)} labels, {len(relationships)} relationships")
#     print(f"[IMAGE_DEBUG] gom_to_llm_text: labels={labels}")
#     print(f"[IMAGE_DEBUG] gom_to_llm_text: relationships={relationships}")

#     lines = []
#     lines.append("Objects:")
#     for i, label in enumerate(labels):
#         name = label.lower().strip().replace(" ", "_")
#         lines.append(f"{i}: {name}")

#     lines.append("\nSpatial relationships:")
#     for rel in relationships:
#         src = rel["src_idx"]
#         tgt = rel["tgt_idx"]
#         relation = rel["relation"]

#         src_name = labels[src].lower().strip().replace(" ", "_")
#         tgt_name = labels[tgt].lower().strip().replace(" ", "_")

#         lines.append(f"{src_name} is {relation} {tgt_name}.")

#     lines.append("\nAssign coordinates to all objects so these relationships are satisfied.")
#     result = "\n".join(lines)
#     print(f"[IMAGE_DEBUG] gom_to_llm_text: built text length={len(result)}")
#     print(f"[IMAGE_DEBUG] gom_to_llm_text: preview={result[:500]!r}")
#     return result

# Run GoM on this image and give me the LLM prompt text.
# def run_gom_and_build_text(image_path, device="cpu"):
#     print("[IMAGE_DEBUG] run_gom_and_build_text: starting")
#     image_path = Path(image_path).resolve()
#     print(f"[IMAGE_DEBUG] run_gom_and_build_text: image_path={image_path}, exists={image_path.exists()}, device={device}")

#     try:
#         print("[IMAGE_DEBUG] run_gom_and_build_text: initializing GoM with YOLO-World DC detector")
#         gom_init_start = time.time()
#         detect_fn = make_dc_detect_fn(device=device)
#         p = GoM(detect_fn=detect_fn, device=device)
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: GoM initialized in {time.time() - gom_init_start:.2f}s")

#         cfg = ProcessingConfig(
#             question="What is in the image?",
#             style="gom_text_labeled",
#             display_labels=False,
#             display_relationships=False,
#             display_relation_labels=False,
#             show_segmentation=False
#         )
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: ProcessingConfig={cfg}")

#         print("[IMAGE_DEBUG] run_gom_and_build_text: calling GoM.process")
#         process_start = time.time()
#         r = p.process(str(image_path), config=cfg, save=False)
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: GoM.process completed in {time.time() - process_start:.2f}s")
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: result keys={list(r.keys())}")
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: num boxes={len(r.get('boxes', []))}")
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: num labels={len(r.get('labels', []))}")
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: num relationships={len(r.get('relationships', []))}")
#         if r.get('processing_time') is not None:
#             print(f"[IMAGE_DEBUG] run_gom_and_build_text: GoM reported processing_time={r.get('processing_time')}")

#         r.pop("output_image", None)
#         return gom_to_llm_text(r)
#     except Exception as e:
#         print(f"[IMAGE_DEBUG] run_gom_and_build_text: EXCEPTION type={type(e).__name__}, message={e!r}")
#         traceback.print_exc()
#         raise


# Run model on the image and return raw structured output.
def run_gom_and_return_result(image_path, device="cpu"): #note we are not using gom model here, we are using YOLO-World model with DC vocab
    print("[IMAGE_DEBUG] run_gom_and_return_result: starting")
    image_path = Path(image_path).resolve()
    print(f"[IMAGE_DEBUG] image_path={image_path}, exists={image_path.exists()}, device={device}")

    try:
        print("[IMAGE_DEBUG] run_gom_and_return_result: initializing GoM with configured detector")
        gom_init_start = time.time()
        detect_fn = make_detect_fn(device=device)
        p = GoM(detect_fn=detect_fn, device=device)
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: GoM initialized in {time.time() - gom_init_start:.2f}s")

        cfg = ProcessingConfig(
            question="What is in the image?",
            style="gom_text_labeled",
            display_labels=False,
            display_relationships=False,
            display_relation_labels=False,
            show_segmentation=False
        )
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: ProcessingConfig={cfg}")

        print("[IMAGE_DEBUG] run_gom_and_return_result: calling GoM.process")
        process_start = time.time()
        r = p.process(str(image_path), config=cfg, save=False)
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: GoM.process completed in {time.time() - process_start:.2f}s")
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: result keys={list(r.keys())}")
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: num boxes={len(r.get('boxes', []))}")
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: num labels={len(r.get('labels', []))}")
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: num relationships={len(r.get('relationships', []))}")
        if r.get('processing_time') is not None:
            print(f"[IMAGE_DEBUG] run_gom_and_return_result: GoM reported processing_time={r.get('processing_time')}")

        r.pop("output_image", None)
        return r

    except Exception as e:
        print(f"[IMAGE_DEBUG] run_gom_and_return_result: EXCEPTION {type(e).__name__}: {e!r}")
        traceback.print_exc()
        raise