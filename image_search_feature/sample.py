import matplotlib
matplotlib.use("Agg")

import time
import traceback
from gom import GoM, ProcessingConfig
from pathlib import Path

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
        print("[IMAGE_DEBUG] run_gom_and_build_text: initializing GoM")
        gom_init_start = time.time()
        p = GoM(device=device)
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
