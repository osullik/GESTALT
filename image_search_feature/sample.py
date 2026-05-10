import matplotlib
matplotlib.use("Agg")

from gom import GoM, ProcessingConfig
from pathlib import Path

def gom_to_llm_text(r):
    labels = r["labels"]
    relationships = r["relationships"]

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
    return "\n".join(lines)

def run_gom_and_build_text(image_path, device="cpu"):
    image_path = Path(image_path)

    p = GoM(device=device)
    cfg = ProcessingConfig(
        question="What is in the image?",
        style="gom_text_labeled",
        display_labels=False,
        display_relationships=False,
        display_relation_labels=False,
        show_segmentation=False
    )
    print("Before process")
    
    r = p.process(str(image_path), config=cfg, save=False)
    
    print("After process")
    
    r.pop("output_image", None)
    return gom_to_llm_text(r)