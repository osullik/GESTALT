import matplotlib
matplotlib.use("Agg")

import time
import threading
import traceback
from gom import GoM, ProcessingConfig
from pathlib import Path

from ultralytics import YOLO

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


def gom_to_llm_text(r):
    print("[IMAGE_DEBUG] gom_to_llm_text: starting")
    labels = r["labels"]
    relationships = r["relationships"]
    print(f"[IMAGE_DEBUG] gom_to_llm_text: {len(labels)} labels, {len(relationships)} relationships")
    print(f"[IMAGE_DEBUG] gom_to_llm_text: labels={labels}")
    print(f"[IMAGE_DEBUG] gom_to_llm_text: relationships={relationships}")

    lines = []
    lines.append("Objects:")
    for i, label in enumerate(labels):
        name = label.lower().strip().replace(" ", "_")
        lines.append(f"{i}: {name}")

    lines.append("\nSpatial relationships:")
    for rel in relationships:
        src = rel["src_idx"]
        tgt = rel["tgt_idx"]
        relation = rel["relation"]

        src_name = labels[src].lower().strip().replace(" ", "_")
        tgt_name = labels[tgt].lower().strip().replace(" ", "_")

        lines.append(f"{src_name} is {relation} {tgt_name}.")

    lines.append("\nAssign coordinates to all objects so these relationships are satisfied.")
    result = "\n".join(lines)
    print(f"[IMAGE_DEBUG] gom_to_llm_text: built text length={len(result)}")
    print(f"[IMAGE_DEBUG] gom_to_llm_text: preview={result[:500]!r}")
    return result

def run_gom_and_build_text(image_path, device="cpu"):
    print("[IMAGE_DEBUG] run_gom_and_build_text: starting")
    image_path = Path(image_path).resolve()
    print(f"[IMAGE_DEBUG] run_gom_and_build_text: image_path={image_path}, exists={image_path.exists()}, device={device}")

    try:
        print("[IMAGE_DEBUG] run_gom_and_build_text: initializing GoM with YOLO-World DC detector")
        gom_init_start = time.time()
        detect_fn = make_dc_detect_fn(device=device)
        p = GoM(detect_fn=detect_fn, device=device)
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: GoM initialized in {time.time() - gom_init_start:.2f}s")

        cfg = ProcessingConfig(
            question="What is in the image?",
            style="gom_text_labeled",
            display_labels=False,
            display_relationships=False,
            display_relation_labels=False,
            show_segmentation=False
        )
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: ProcessingConfig={cfg}")

        print("[IMAGE_DEBUG] run_gom_and_build_text: calling GoM.process")
        process_start = time.time()
        r = p.process(str(image_path), config=cfg, save=False)
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: GoM.process completed in {time.time() - process_start:.2f}s")
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: result keys={list(r.keys())}")
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: num boxes={len(r.get('boxes', []))}")
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: num labels={len(r.get('labels', []))}")
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: num relationships={len(r.get('relationships', []))}")
        if r.get('processing_time') is not None:
            print(f"[IMAGE_DEBUG] run_gom_and_build_text: GoM reported processing_time={r.get('processing_time')}")

        r.pop("output_image", None)
        return gom_to_llm_text(r)
    except Exception as e:
        print(f"[IMAGE_DEBUG] run_gom_and_build_text: EXCEPTION type={type(e).__name__}, message={e!r}")
        traceback.print_exc()
        raise
