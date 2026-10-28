import json
import os
import pickle
import random
import re
import sys
import tempfile
import time
import traceback
from collections import defaultdict, deque
from pathlib import Path

import pandas as pd
from django.shortcuts import render
from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response


# ---------------------------------------------------------------------------
# Import paths for the existing GESTALT project structure.
# ---------------------------------------------------------------------------

sys.path.insert(1, os.getcwd() + "/../../code/")
sys.path.insert(1, os.getcwd() + "/../../data/")
sys.path.insert(1, os.path.join(os.getcwd(), "media"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)

from conceptMapping import ConceptMapper
from image_search_feature.sample import run_gom_and_return_result
from search import InvertedIndex


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_REGIONS = [
    "Swan Valley, Australia",
    "Washington D.C., USA",
    "Hamburg, Germany",
]

REGION_DATA_FILES = {
    "Swan Valley, Australia": {
        "folder": "SV",
        "log": "Region set to SV.............",
    },
    "Washington D.C., USA": {
        "folder": "DC",
        "log": "Region set to DC.............",
    },
    "Hamburg, Germany": {
        "folder": "HAM",
        "log": "Region set to Hamburg.............",
    },
}

CANVAS_SIZE = 1000
REL_STEP = 180
REL_MARGIN = 40
MAX_BFS_PASSES = 20


# ---------------------------------------------------------------------------
# Basic view/session endpoints
# ---------------------------------------------------------------------------

def index(request):
    request.session["box_data"] = pickle.dumps({}).hex()
    request.session["REGIONS"] = DEFAULT_REGIONS
    request.session["objects_changed"] = False
    return render(request, "draggable/index.html")


@api_view(["GET"])
def get_regions(request):
    if "REGIONS" not in request.session:
        request.session["REGIONS"] = DEFAULT_REGIONS

    return Response({"regions": request.session["REGIONS"]})


@api_view(["POST"])
def set_region(request):
    request.session["region"] = request.data.get("name")
    print("Region selection has been set to.... ", request.session["region"])

    set_data_structure_paths(request)
    return Response({"success": True})


@api_view(["GET"])
def get_objects(request):
    inverted_index = InvertedIndex(request.session["INVERTED_INDEX"])
    request.session["VOCAB"] = list(inverted_index.ii.keys())
    print("VOCAB is:", request.session["VOCAB"])

    return Response({"objects": request.session["VOCAB"]})


@api_view(["POST"])
def set_search_params(request):
    request.session["object_query"] = request.data.get("object_query")
    request.session["search_type"] = request.data.get("search_type")
    request.session["cardinality_invariant"] = (
        request.data.get("knows_cardinality") == "false"
    )
    request.session["canvas_center"] = request.data.get("canvas_center")

    print("Query was...", request.session["object_query"])
    print("Canvas center is...", request.session["canvas_center"])

    return Response({"success": True})


# ---------------------------------------------------------------------------
# Object/vocab helpers
# ---------------------------------------------------------------------------

def normalize_object_name(name):
    return str(name).lower().strip().replace(" ", "_")


def resolve_to_vocab_label(name, valid_objects):
    normalized_name = normalize_object_name(name)

    if normalized_name in valid_objects:
        return normalized_name

    base_name = re.sub(r"_\d+$", "", normalized_name)
    if base_name != normalized_name and base_name in valid_objects:
        return base_name

    return None

def prune_invalid_objects(request, objects_dict):
    valid_objects = set(request.session.get("VOCAB", []))
    print(
        "[IMAGE_DEBUG] prune_invalid_objects: "
        f"input count={len(objects_dict)}, vocab size={len(valid_objects)}"
    )

    pruned = {}

    for key, obj in objects_dict.items():
        raw_name = obj["name"]
        vocab_label = resolve_to_vocab_label(raw_name, valid_objects)

        if vocab_label is None:
            print(
                "[IMAGE_DEBUG] prune_invalid_objects: "
                f"pruned invalid object={normalize_object_name(raw_name)!r}"
            )
            continue

        if vocab_label != normalize_object_name(raw_name):
            print(
                "[IMAGE_DEBUG] prune_invalid_objects: "
                f"resolved {raw_name!r} -> {vocab_label!r}"
            )

        pruned[key] = {
            **obj,
            "name": vocab_label,
        }

    return pruned


# ---------------------------------------------------------------------------
# GoM image-to-canvas algorithm
# ---------------------------------------------------------------------------

def get_box_center(box):
    if isinstance(box, dict):
        x1 = box.get("x1", box.get("xmin", box.get("left", 0)))
        y1 = box.get("y1", box.get("ymin", box.get("top", 0)))
        x2 = box.get("x2", box.get("xmax", box.get("right", x1)))
        y2 = box.get("y2", box.get("ymax", box.get("bottom", y1)))
        return (x1 + x2) / 2, (y1 + y2) / 2

    if isinstance(box, (list, tuple)) and len(box) >= 4:
        x1, y1, x2, y2 = box[:4]
        return (x1 + x2) / 2, (y1 + y2) / 2

    return 0, 0


def clamp(value, min_value=0, max_value=CANVAS_SIZE):
    return max(min_value, min(max_value, value))


def scale_detected_locations_to_canvas(gom_result, canvas_size=CANVAS_SIZE):
    labels = gom_result.get("labels", [])
    boxes = gom_result.get("boxes", [])

    if not labels:
        return {}

    centers = []
    for i, _label in enumerate(labels):
        if i < len(boxes):
            centers.append(get_box_center(boxes[i]))
        else:
            centers.append((random.randint(100, 900), random.randint(100, 900)))

    xs = [center[0] for center in centers]
    ys = [center[1] for center in centers]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max(max_x - min_x, 1)
    height = max(max_y - min_y, 1)

    objects = {}
    for i, label in enumerate(labels):
        cx, cy = centers[i]
        scaled_x = ((cx - min_x) / width) * canvas_size
        scaled_y = ((cy - min_y) / height) * canvas_size

        objects[str(i)] = {
            "name": normalize_object_name(label),
            "x": clamp(scaled_x, max_value=canvas_size),
            "y": clamp(scaled_y, max_value=canvas_size),
            "moved": False,
        }

    return objects


def relation_is_satisfied(h_obj, t_obj, relation, margin=REL_MARGIN):
    hx, hy = h_obj["x"], h_obj["y"]
    tx, ty = t_obj["x"], t_obj["y"]
    relation = normalize_object_name(relation)

    if relation in {"left", "left_of", "to_left_of"}:
        return hx < tx - margin

    if relation in {"right", "right_of", "to_right_of"}:
        return hx > tx + margin

    if relation in {"above", "over", "north", "in_front_of", "front"}:
        return hy < ty - margin

    if relation in {"below", "under", "south", "behind"}:
        return hy > ty + margin

    if relation in {"near", "next_to", "beside"}:
        distance = ((hx - tx) ** 2 + (hy - ty) ** 2) ** 0.5
        return distance <= REL_STEP * 1.5

    return True


def desired_position_from_relation(anchor_obj, relation, step=REL_STEP):
    tx, ty = anchor_obj["x"], anchor_obj["y"]
    relation = normalize_object_name(relation)

    if relation in {"left", "left_of", "to_left_of"}:
        return tx - step, ty

    if relation in {"right", "right_of", "to_right_of"}:
        return tx + step, ty

    if relation in {"above", "over", "north", "in_front_of", "front"}:
        return tx, ty - step

    if relation in {"below", "under", "south", "behind"}:
        return tx, ty + step

    if relation in {"near", "next_to", "beside"}:
        return tx + step, ty

    return tx, ty


def opposite_relation(relation):
    relation = normalize_object_name(relation)
    opposites = {
        "left": "right",
        "left_of": "right_of",
        "to_left_of": "to_right_of",
        "right": "left",
        "right_of": "left_of",
        "to_right_of": "to_left_of",
        "above": "below",
        "over": "below",
        "north": "south",
        "in_front_of": "behind",
        "front": "behind",
        "below": "above",
        "under": "above",
        "south": "north",
        "behind": "in_front_of",
        "near": "near",
        "next_to": "next_to",
        "beside": "beside",
    }
    return opposites.get(relation, relation)


def build_relationship_graph(relationships):
    graph = defaultdict(list)

    for rel in relationships:
        src = str(rel["src_idx"])
        tgt = str(rel["tgt_idx"])
        relation = rel["relation"]

        edge = {
            "src": src,
            "tgt": tgt,
            "relation": relation,
        }

        graph[src].append(edge)
        graph[tgt].append(edge)

    return graph


def filter_relationships_for_objects(relationships, objects):
    """
    Keep only relationships whose source and target objects still exist.

    After vocab pruning, some detected objects may be removed. Any relationship
    connected to a removed object should also be removed from the final debug
    output/API response.
    """

    valid_object_ids = set(objects.keys())
    pruned_relationships = []

    for rel in relationships:
        src = str(rel.get("src_idx"))
        tgt = str(rel.get("tgt_idx"))

        if src in valid_object_ids and tgt in valid_object_ids:
            pruned_relationships.append(rel)

    return pruned_relationships


def print_relationships_for_objects(title, relationships, objects):
    print(f"[IMAGE_DEBUG] {title} count={len(relationships)}")

    if not relationships:
        print(f"[IMAGE_DEBUG] {title}: none")
        return

    for rel in relationships:
        src = str(rel.get("src_idx"))
        tgt = str(rel.get("tgt_idx"))
        relation = rel.get("relation", "unknown")

        src_obj = objects.get(src)
        tgt_obj = objects.get(tgt)
        src_name = src_obj.get("name", f"unknown_{src}") if src_obj else f"unknown_{src}"
        tgt_name = tgt_obj.get("name", f"unknown_{tgt}") if tgt_obj else f"unknown_{tgt}"

        distance = rel.get("distance")
        confidence = rel.get("confidence")
        distance_text = f"{distance:.1f}" if distance is not None else "N/A"
        confidence_text = f"{confidence:.2f}" if confidence is not None else "N/A"

        if src_obj and tgt_obj:
            satisfied = relation_is_satisfied(src_obj, tgt_obj, relation)
            satisfied_text = "yes" if satisfied else "no"
            position_text = (
                f"src=({src_obj['x']:.1f}, {src_obj['y']:.1f}) "
                f"tgt=({tgt_obj['x']:.1f}, {tgt_obj['y']:.1f})"
            )
        else:
            satisfied_text = "N/A"
            position_text = "missing endpoint"

        print(
            f"rel: {src}:{src_name} {relation} "
        )


def get_neighbors_from_graph(graph, node_id):
    node_id = str(node_id)
    neighbors = set()

    for edge in graph.get(node_id, []):
        src = edge["src"]
        tgt = edge["tgt"]
        neighbors.add(tgt if src == node_id else src)

    return neighbors


def expand_to_moved_objects_and_neighbors(moved_ids, graph):
    next_nodes = set(moved_ids)

    for moved_id in moved_ids:
        next_nodes.update(get_neighbors_from_graph(graph, moved_id))

    return next_nodes


def move_object_to_satisfy_relation(objects, src, tgt, relation, moved_this_pass):
    h_obj = objects[src]
    t_obj = objects[tgt]

    if relation_is_satisfied(h_obj, t_obj, relation):
        return None

    if src not in moved_this_pass:
        new_x, new_y = desired_position_from_relation(t_obj, relation)
        h_obj["x"] = clamp(new_x)
        h_obj["y"] = clamp(new_y)
        h_obj["moved"] = True
        return src

    if tgt not in moved_this_pass:
        new_x, new_y = desired_position_from_relation(
            h_obj,
            opposite_relation(relation),
        )
        t_obj["x"] = clamp(new_x)
        t_obj["y"] = clamp(new_y)
        t_obj["moved"] = True
        return tgt

    return None


def bfs_relationship_pass(objects, relationships, active_nodes=None):
    graph = build_relationship_graph(relationships)
    active_nodes = set(objects.keys()) if active_nodes is None else {
        str(node) for node in active_nodes if str(node) in objects
    }

    moved_this_pass = set()
    visited = set()
    remaining = list(active_nodes)

    while remaining:
        start = random.choice(remaining)
        queue = deque([start])

        while queue:
            current = queue.popleft()

            if current in visited or current not in active_nodes:
                continue

            visited.add(current)

            for edge in graph.get(current, []):
                src = edge["src"]
                tgt = edge["tgt"]
                relation = edge["relation"]

                if src not in objects or tgt not in objects:
                    continue

                if src not in active_nodes or tgt not in active_nodes:
                    continue

                moved_id = move_object_to_satisfy_relation(
                    objects,
                    src,
                    tgt,
                    relation,
                    moved_this_pass,
                )

                if moved_id is not None:
                    moved_this_pass.add(moved_id)

                neighbor = tgt if current == src else src
                if neighbor not in visited and neighbor in active_nodes:
                    queue.append(neighbor)

        remaining = [node for node in active_nodes if node not in visited]

    return moved_this_pass


def satisfy_gom_relationships_with_bfs(
    objects,
    relationships,
    max_passes=MAX_BFS_PASSES,
):
    if not objects:
        return objects

    graph = build_relationship_graph(relationships)
    active_nodes = set(objects.keys())

    for pass_num in range(max_passes):
        print(
            f"[IMAGE_DEBUG] BFS pass {pass_num + 1}: "
            f"active_nodes={sorted(active_nodes)}"
        )

        for obj in objects.values():
            obj["moved"] = False

        moved_this_pass = bfs_relationship_pass(
            objects,
            relationships,
            active_nodes=active_nodes,
        )

        print(
            f"[IMAGE_DEBUG] BFS pass {pass_num + 1}: "
            f"moved={sorted(moved_this_pass)}"
        )

        if not moved_this_pass:
            print("[IMAGE_DEBUG] BFS stable: no objects moved")
            break

        active_nodes = expand_to_moved_objects_and_neighbors(moved_this_pass, graph)

    return objects


def construct_query_from_gom_algorithm(request, gom_result):
    print("\n[IMAGE_DEBUG] ===== construct_query_from_gom_algorithm: START =====")

    objects = scale_detected_locations_to_canvas(gom_result)
    relationships = gom_result.get("relationships", [])

    print(f"[IMAGE_DEBUG] initial objects count={len(objects)}")
    for obj_id, obj in objects.items():
        print(
            f"[IMAGE_DEBUG]   obj {obj_id}: "
            f"{obj['name']} at ({obj['x']:.1f}, {obj['y']:.1f})"
        )

    print_relationships_for_objects(
        "relationships before pruning",
        relationships,
        objects,
    )

    objects = satisfy_gom_relationships_with_bfs(objects, relationships)

    for obj in objects.values():
        obj.pop("moved", None)

    print(f"[IMAGE_DEBUG] objects after BFS count={len(objects)}")
    for obj_id, obj in objects.items():
        print(
            f"[IMAGE_DEBUG]   after BFS obj {obj_id}: "
            f"{obj['name']} at ({obj['x']:.1f}, {obj['y']:.1f})"
        )

    objects = prune_invalid_objects(request, objects)
    relationships_after_pruning = filter_relationships_for_objects(
        relationships,
        objects,
    )

    print(f"[IMAGE_DEBUG] final objects after pruning count={len(objects)}")
    for obj_id, obj in objects.items():
        print(
            f" final obj {obj_id}: "
            f"{obj['name']} at ({obj['x']:.1f}, {obj['y']:.1f})"
        )

    print_relationships_for_objects(
        "relationships after pruning",
        relationships_after_pruning,
        objects,
    )

    print("[IMAGE_DEBUG] ===== construct_query_from_gom_algorithm: END =====\n")
    return objects


# ---------------------------------------------------------------------------
# LLM text-to-canvas flow
# ---------------------------------------------------------------------------

def _parse_object_locations_from_completion(completion):
    message = completion.choices[0].message
    print(f"[IMAGE_DEBUG] _parse_object_locations: message.content={message.content!r}")
    print(
        "[IMAGE_DEBUG] _parse_object_locations: "
        f"message.parsed={getattr(message, 'parsed', None)!r}"
    )

    parsed = getattr(message, "parsed", None)
    if parsed is not None:
        if hasattr(parsed, "object_locations"):
            return parsed.object_locations
        if isinstance(parsed, dict) and "object_locations" in parsed:
            return parsed["object_locations"]

    if not message.content:
        raise ValueError("LLM returned empty content")

    raw_result = json.loads(message.content)
    if isinstance(raw_result, dict) and "object_locations" in raw_result:
        return raw_result["object_locations"]

    if (
        isinstance(raw_result, dict)
        and raw_result.get("type") == "object"
        and "properties" in raw_result
    ):
        raise ValueError(
            "LLM returned the JSON schema definition instead of object location "
            "data. Retry the request or adjust the prompt."
        )

    keys = list(raw_result.keys()) if isinstance(raw_result, dict) else type(raw_result)
    raise KeyError(f"LLM response missing 'object_locations' key. Got keys: {keys}")


def construct_query_from_llm(request):
    print("[IMAGE_DEBUG] construct_query_from_llm: starting")

    openai_api_key = request.session.get("api_key")
    print(
        "[IMAGE_DEBUG] construct_query_from_llm: "
        f"api_key present={bool(openai_api_key)}, "
        f"length={len(openai_api_key) if openai_api_key else 0}"
    )

    if not openai_api_key:
        raise ValueError("No API key provided")

    client = OpenAI(api_key=openai_api_key, base_url="https://api.openai.com/v1")
    query_text = request.session["query_text"]

    print(f"[IMAGE_DEBUG] construct_query_from_llm: query_text length={len(query_text)}")
    print(f"[IMAGE_DEBUG] construct_query_from_llm: query_text preview={query_text[:500]!r}")

    system_prompt = (
        "You are tasked with providing coordinates for objects given a textual "
        "description of their position. For each object, return coordinates where "
        "each coordinate ranges from -10 to 10. For orientation, larger y values "
        "are North/frontwards."
    )

    print(
        "[IMAGE_DEBUG] construct_query_from_llm: "
        "calling OpenAI chat.completions.parse (model=gpt-5-nano)"
    )
    llm_start = time.time()
    completion = client.chat.completions.parse(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_text},
        ],
        model="gpt-5-nano",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "object_locations_schema",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "object_locations": {
                            "type": "array",
                            "description": (
                                "List of detected or specified objects with "
                                "coordinates."
                            ),
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "number"},
                                    "name": {"type": "string"},
                                    "x": {"type": "number"},
                                    "y": {"type": "number"},
                                },
                                "required": ["id", "name", "x", "y"],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["object_locations"],
                    "additionalProperties": False,
                },
            },
        },
    )
    print(
        "[IMAGE_DEBUG] construct_query_from_llm: "
        f"OpenAI call completed in {time.time() - llm_start:.2f}s"
    )

    object_locations = _parse_object_locations_from_completion(completion)
    print(f"[IMAGE_DEBUG] construct_query_from_llm: object_locations={object_locations}")

    objects_dict = {}
    for res in object_locations:
        objects_dict[str(res["id"])] = {
            "name": normalize_object_name(res["name"]),
            "x": (res["x"] + 10) * 50,
            "y": (res["y"] + 10) * 50,
        }

    print(f"[IMAGE_DEBUG] construct_query_from_llm: objects before pruning={objects_dict}")
    objects_dict = prune_invalid_objects(request, objects_dict)
    print(f"[IMAGE_DEBUG] construct_query_from_llm: objects after pruning={objects_dict}")
    print(
        "[IMAGE_DEBUG] construct_query_from_llm: "
        f"done, returning {len(objects_dict)} objects"
    )

    return objects_dict


@api_view(["POST"])
def generate_objects_from_text(request):
    request.session["api_key"] = request.data.get("api_key", "")
    request.session["query_text"] = request.data.get("text_input", "")

    objects_dict = construct_query_from_llm(request)
    request.session["objects_changed"] = True

    return Response({"objects": objects_dict, "success": True})


# ---------------------------------------------------------------------------
# Data path and search helpers
# ---------------------------------------------------------------------------

def set_data_structure_paths(request):
    data_directory = ""
    for path in sys.path:
        if path.endswith("media"):
            data_directory = path
            break

    assert data_directory in sys.path, "Unable to find the 'GESTALT/data' directory"

    region = request.session["region"]
    region_config = REGION_DATA_FILES.get(region)

    if region_config is None:
        print("UNRECOGNIZED REGION SELECTED")
        return

    region_folder = region_config["folder"]
    print(region_config["log"])

    output_path = os.path.join(data_directory, "data", region_folder, "output")
    request.session["CONCEPT_MAPS_PATH"] = os.path.join(
        output_path,
        "concept_mapping",
        "ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl",
    )
    request.session["INVERTED_INDEX"] = os.path.join(
        output_path,
        "ownershipAssignment",
        "DBSCAN_PredictedLocations_FT=0.0.csv",
    )
    request.session["LOCATION_STRUCTURE_PATH"] = os.path.join(
        output_path,
        "concept_mapping",
        "RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON",
    )


def parse_query_from_dict(query_dict):
    flat_dict = {
        "name": [],
        "longitude": [],
        "latitude": [],
        "predicted_location": [],
    }

    for obj in query_dict.values():
        flat_dict["name"].append(obj["name"])
        flat_dict["longitude"].append(obj["x"])
        flat_dict["latitude"].append(obj["y"])
        flat_dict["predicted_location"].append("PICTORIAL_QUERY")

    return pd.DataFrame.from_dict(flat_dict, orient="columns")


def obj_obj_search(request, query_df, card_invariance):
    concept_mapper = ConceptMapper()
    queries_dict = concept_mapper.createConceptMap(
        input_df=query_df,
        inputFile=None,
        cm_type="query",
    )

    with open(request.session["CONCEPT_MAPS_PATH"], "rb") as in_file:
        concept_maps = pickle.load(in_file)

    results = set()

    for query in queries_dict.values():
        lon_order, lat_order = query[1]
        search_order = concept_mapper.getSearchOrder(lon_order, lat_order)
        print("SEARCHING FOR THIS searchOrder: ", search_order)

        for location_cm, concept_map in concept_maps.items():
            if concept_mapper.searchMatrix(concept_map, search_order.copy()):
                results.add(location_cm)

    return list(results)


def obj_loc_search(request, query_df, card_invariance, canvas_center):
    return None


def search(request, query_df):
    print("SEARCH TYPE IS: ", request.session["search_type"])
    print("CARDINALITY INVARIANT: ", request.session["cardinality_invariant"])

    if request.session["search_type"] == "Object":
        print("\n\n= = = = = = = = =  OBJECT CENTRIC SEARCH = = = = = = = = = \n")
        return obj_obj_search(
            request,
            query_df,
            card_invariance=request.session["cardinality_invariant"],
        )

    if request.session["search_type"] == "Location":
        print("\n\n= = = = = = = = =  LOCATION CENTRIC SEARCH = = = = = = = = = \n")
        return obj_loc_search(
            request,
            query_df,
            card_invariance=request.session["cardinality_invariant"],
            canvas_center=request.session["canvas_center"],
        )

    print("UNRECOGNIZED SEARCH TYPE")
    return None


@api_view(["GET"])
def get_search_result(request):
    request.session["objects_changed"] = False

    query_dict = json.loads(request.session["object_query"])
    query_df = parse_query_from_dict(query_dict)
    print(query_df)

    results = search(request, query_df)

    if not results:
        print("No Results Found")
    else:
        print("Found Following Matches to Query:")
        for result in results:
            print(result)

    response_data = {"locations": results if results else []}
    print(response_data)
    return Response(response_data)


# ---------------------------------------------------------------------------
# Image upload endpoint
# ---------------------------------------------------------------------------

@api_view(["POST"])
def generate_objects_from_image(request):
    request_start = time.time()
    print("[IMAGE_DEBUG] generate_objects_from_image: request received")
    print(
        "[IMAGE_DEBUG] generate_objects_from_image: "
        f"method={request.method}, content_type={request.content_type}"
    )
    print(f"[IMAGE_DEBUG] generate_objects_from_image: FILES keys={list(request.FILES.keys())}")
    print(f"[IMAGE_DEBUG] generate_objects_from_image: DATA keys={list(request.data.keys())}")
    print(
        "[IMAGE_DEBUG] generate_objects_from_image: "
        f"session keys={list(request.session.keys())}"
    )
    print(f"[IMAGE_DEBUG] generate_objects_from_image: cwd={os.getcwd()}")

    if "image" not in request.FILES:
        print("[IMAGE_DEBUG] generate_objects_from_image: ERROR no image in request.FILES")
        return Response({"error": "No image provided"}, status=400)

    image = request.FILES["image"]
    print(
        "[IMAGE_DEBUG] generate_objects_from_image: "
        f"image name={image.name!r}, size={image.size}, content_type={image.content_type}"
    )

    temp_path = None

    try:
        suffix = Path(image.name).suffix or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = Path(temp_file.name)
            bytes_written = 0

            for chunk in image.chunks():
                temp_file.write(chunk)
                bytes_written += len(chunk)

        print(
            "[IMAGE_DEBUG] generate_objects_from_image: "
            f"wrote {bytes_written} bytes to {temp_path}, exists={temp_path.exists()}"
        )

        gom_result = run_gom_and_return_result(temp_path)
        objects_dict = construct_query_from_gom_algorithm(request, gom_result)
        relationships_after_pruning = filter_relationships_for_objects(
            gom_result.get("relationships", []),
            objects_dict,
        )

        request.session["objects_changed"] = True
        print(
            "[IMAGE_DEBUG] generate_objects_from_image: "
            f"success, total time={time.time() - request_start:.2f}s"
        )

        return Response(
            {
                "objects": objects_dict,
                "gom_relationships": relationships_after_pruning,
                "raw_gom_relationships": gom_result.get("relationships", []),
                "success": True,
            }
        )

    except Exception as exc:
        print(
            "[IMAGE_DEBUG] generate_objects_from_image: "
            f"EXCEPTION type={type(exc).__name__}, message={exc!r}"
        )
        traceback.print_exc()
        return Response({"error": str(exc)}, status=500)

    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
            print(f"[IMAGE_DEBUG] generate_objects_from_image: deleted temp file {temp_path}")