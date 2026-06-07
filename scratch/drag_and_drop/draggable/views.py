from aiohttp import request
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import sys
import os
import re
import pickle
import traceback
import time
import pandas as pd
import json

from pathlib import Path

sys.path.insert(1, os.getcwd()+"/../../code/")
sys.path.insert(1, os.getcwd()+"/../../data/")
sys.path.insert(1, os.path.join(os.getcwd(),"media"))

from conceptMapping import ConceptMapper
from search import InvertedIndex
from openai import OpenAI, api_key
import json

# print(os.environ["OPENAI_API_KEY"])

# OAI_CLIENT = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
#                     base_url="https://us.api.openai.com/v1")

import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)
from image_search_feature.sample import run_gom_and_build_text

def index(request):
    # Initialize query object data as empty
    request.session['box_data'] = pickle.dumps({}).hex()
    request.session['REGIONS'] = ["Swan Valley, Australia", "Washington D.C., USA", "Hamburg, Germany"]
    request.session['objects_changed'] = False
    return render(request, 'draggable/index.html')

@api_view(['GET'])
def get_regions(request):
    # Initialize regions in session if not present
    if 'REGIONS' not in request.session:
        request.session['REGIONS'] = ["Swan Valley, Australia", "Washington D.C., USA", "Hamburg, Germany"]
    
    response_data = {
        'regions': request.session['REGIONS']
    }
    return Response(response_data)

def normalize_object_name(name):
    return name.lower().strip().replace(" ", "_")

def resolve_to_vocab_label(name, valid_objects):
    """
    Map a GoM/LLM object label to a canonical VOCAB entry.

    GoM may append numeric instance suffixes (e.g. bus_stop_1, bus_stop_2).
    VOCAB stores the base label (e.g. bus_stop). Strip only trailing _<digits>
    and return the matching VOCAB label for canvas display.
    """
    normalized_name = normalize_object_name(name)

    if normalized_name in valid_objects:
        return normalized_name

    base_name = re.sub(r"_\d+$", "", normalized_name)
    if base_name != normalized_name and base_name in valid_objects:
        return base_name

    return None

def prune_invalid_objects(request, objects_dict):
    valid_objects = set(request.session.get('VOCAB', []))
    print(f"[IMAGE_DEBUG] prune_invalid_objects: input count={len(objects_dict)}, vocab size={len(valid_objects)}")

    pruned = {}

    for key, obj in objects_dict.items():
        raw_name = obj["name"]
        vocab_label = resolve_to_vocab_label(raw_name, valid_objects)

        if vocab_label is not None:
            if vocab_label != normalize_object_name(raw_name):
                print(f"[IMAGE_DEBUG] prune_invalid_objects: resolved {raw_name!r} -> {vocab_label!r}")
            pruned[key] = {
                **obj,
                "name": vocab_label
            }
        else:
            print(f"[IMAGE_DEBUG] prune_invalid_objects: pruned invalid object={normalize_object_name(raw_name)!r}")

    return pruned

def _parse_object_locations_from_completion(completion):
    message = completion.choices[0].message
    print(f"[IMAGE_DEBUG] _parse_object_locations: message.content={message.content!r}")
    print(f"[IMAGE_DEBUG] _parse_object_locations: message.parsed={getattr(message, 'parsed', None)!r}")

    parsed = getattr(message, 'parsed', None)
    if parsed is not None:
        if hasattr(parsed, 'object_locations'):
            return parsed.object_locations
        if isinstance(parsed, dict) and 'object_locations' in parsed:
            return parsed['object_locations']

    if not message.content:
        raise ValueError("LLM returned empty content")

    raw_result = json.loads(message.content)
    if isinstance(raw_result, dict) and 'object_locations' in raw_result:
        return raw_result['object_locations']

    if isinstance(raw_result, dict) and raw_result.get('type') == 'object' and 'properties' in raw_result:
        raise ValueError(
            "LLM returned the JSON schema definition instead of object location data. "
            "Retry the request or adjust the prompt."
        )

    raise KeyError(f"LLM response missing 'object_locations' key. Got keys: {list(raw_result.keys()) if isinstance(raw_result, dict) else type(raw_result)}")

def construct_query_from_llm(request):
    print("[IMAGE_DEBUG] construct_query_from_llm: starting")
    api_key = request.session.get('api_key')
    print(f"[IMAGE_DEBUG] construct_query_from_llm: api_key present={bool(api_key)}, length={len(api_key) if api_key else 0}")
    client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
    query_text = request.session['query_text']
    print(f"[IMAGE_DEBUG] construct_query_from_llm: query_text length={len(query_text)}")
    print(f"[IMAGE_DEBUG] construct_query_from_llm: query_text preview={query_text[:500]!r}")

    SYSTEM_PROMPT = "You are tasked with providing coordinates for objects given a textual description of their position. For each object, return coordinates for it where each coordinate ranges from -10 to 10. For orientation, larger y values are North/frontwards. The objects will be together in a large textual description of all of their positions. Respond in the form id: {{id}}\n\nobject name: {{object name}}\n\ncoordinates: (x, y)."
    
    print("[IMAGE_DEBUG] construct_query_from_llm: calling OpenAI chat.completions.parse (model=gpt-5-nano)")
    llm_start = time.time()
    completion = client.chat.completions.parse(
            messages=[
                        {
                            "role": "system", 
                            "content": SYSTEM_PROMPT},
                        {
                            "role": "user", 
                            "content": query_text}
                    ],
            model="gpt-5-nano",          #Set the model to use
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
                        "description": "List of detected or specified objects with coordinates.",
                        "items": {
                            "type": "object",
                            "properties": {
                            "id": {
                                "type": "number",
                                "description": "Unique numeric identifier for the object."
                            },
                            "name": {
                                "type": "string",
                                "description": "Name or label of the object."
                            },
                            "x": {
                                "type": "number",
                                "description": "X-coordinate of the object location."
                            },
                            "y": {
                                "type": "number",
                                "description": "Y-coordinate of the object location."
                            }
                            },
                            "required": ["id", "name", "x", "y"],
                            "additionalProperties": False
                        }
                        }
                    },
                    "required": ["object_locations"],
                    "additionalProperties": False
                    }
                }
                }

    )
    print(f"[IMAGE_DEBUG] construct_query_from_llm: OpenAI call completed in {time.time() - llm_start:.2f}s")

    object_locations = _parse_object_locations_from_completion(completion)
    print(f"[IMAGE_DEBUG] construct_query_from_llm: object_locations={object_locations}")

    res_dict = {}

    for res in object_locations:
        res_dict[str(res['id'])] = {
            "name": res['name'].lower().strip().replace(" ", "_"),
            "x": (res['x'] + 10) * 50,
            "y": (res['y'] + 10) * 50
        }

    print(f"[IMAGE_DEBUG] construct_query_from_llm: objects before pruning={res_dict}")
    res_dict = prune_invalid_objects(request, res_dict)
    print(f"[IMAGE_DEBUG] construct_query_from_llm: objects after pruning={res_dict}")
    print(f"[IMAGE_DEBUG] construct_query_from_llm: done, returning {len(res_dict)} objects")

    return res_dict

def set_data_structure_paths(request):
    dataDirectory = ""
    for p in sys.path:
        if p.endswith("media"):
            dataDirectory = p 

    assert (dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory"
        
    # Set data file paths based on region choice
    if request.session['region'] == "Swan Valley, Australia":
        print("Region set to SV.............")
        request.session['CONCEPT_MAPS_PATH'] = os.path.join(dataDirectory,'data', 'SV', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
        request.session['INVERTED_INDEX'] = os.path.join(dataDirectory,'data', 'SV', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
        request.session['LOCATION_STRUCTURE_PATH'] = os.path.join(dataDirectory,'data', 'SV', 'output', 'concept_mapping', 'RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON')
    elif request.session['region'] == "Washington D.C., USA":
        print("Region set to DC.............")
        request.session['CONCEPT_MAPS_PATH'] = os.path.join(dataDirectory,'data', 'DC', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
        request.session['INVERTED_INDEX'] = os.path.join(dataDirectory,'data', 'DC', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
        request.session['LOCATION_STRUCTURE_PATH'] = os.path.join(dataDirectory,'data', 'DC', 'output', 'concept_mapping', 'RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON')
    elif request.session['region'] == "Hamburg, Germany":
        print("Region set to Hamburg.............")
        request.session['CONCEPT_MAPS_PATH'] = os.path.join(dataDirectory,'data', 'HAM', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
        request.session['INVERTED_INDEX'] = os.path.join(dataDirectory,'data', 'HAM', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
        request.session['LOCATION_STRUCTURE_PATH'] = os.path.join(dataDirectory,'data', 'HAM', 'output', 'concept_mapping', 'RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON')
    else:
        print("UNRECOGNIZED REGION SELECTED")

@api_view(['POST'])
def set_region(request):
    request.session['region'] = request.data.get('name')
    print("Region selection has been set to.... ", request.session['region'])

    set_data_structure_paths(request)

    response_data = {'success': True}
    return Response(response_data)
    

@api_view(['GET'])
def get_objects(request):
    # Load data structures using file paths saved in request session
    invertedIndex = InvertedIndex(request.session['INVERTED_INDEX'])
    request.session['VOCAB'] = list(invertedIndex.ii.keys())
    print('VOCAB is:', request.session['VOCAB'])

    response_data = {
        'objects': request.session['VOCAB']
    }
    return Response(response_data)

@api_view(['POST'])
def set_search_params(request):
    request.session['object_query'] = request.data.get('object_query')
    request.session['search_type'] = request.data.get('search_type')
    request.session['cardinality_invariant'] = (request.data.get('knows_cardinality') == 'false')
    request.session['canvas_center'] = request.data.get('canvas_center')

    print("Query was...", request.session['object_query'])
    print("Canvas center is...", request.data.get('canvas_center'))

    response_data = {'success': True}
    return Response(response_data)
    
def parse_query_from_dict(query_dict):
    # Create query dataframe from everything in box_data  
    flatDict = {"name":[], "longitude":[], "latitude":[], "predicted_location":[]}

    for key in query_dict.keys():
        flatDict["name"].append(query_dict[key]["name"])
        flatDict["longitude"].append(query_dict[key]["x"])
        flatDict["latitude"].append(query_dict[key]["y"])
        flatDict["predicted_location"].append("PICTORIAL_QUERY")
    
    query_df = pd.DataFrame.from_dict(flatDict, orient='columns')
    return query_df

def obj_obj_search(request, query_df, card_invariance):
    CM = ConceptMapper()
    queriesDict = CM.createConceptMap(input_df=query_df, inputFile=None, cm_type='query')
    for key in queriesDict.keys():
        lonOrder, latOrder = queriesDict[key][1]
        searchOrder = CM.getSearchOrder(lonOrder, latOrder)
        print("SEARCHING FOR THIS searchOrder: ", searchOrder)

        with open(request.session['CONCEPT_MAPS_PATH'], "rb") as inFile:
            conceptMaps = pickle.load(inFile)
    
    results = []
    for locationCM in conceptMaps.keys():
        # TODO need to use card_invariance flag in COMPASS search fcn
        result = CM.searchMatrix(conceptMaps[locationCM], searchOrder.copy())
        if result == True: 
            results.append(locationCM)
            result = False

    return results

def obj_loc_search(request, query_df, card_invariance, canvas_center):
        #with open(request.session['LOCATION_STRUCTURE_PATH'], "r") as inFile:
        #    referenceLocations = json.load(inFile)
        # TODO make COMPASS seacrh function and call it here
    return None

def search(request, query_df):
    print("SEARCH TYPE IS: ", request.session['search_type'])
    print("CARDINALITY INVARIANT: ", request.session['cardinality_invariant'])

    if request.session['search_type'] == "Object":
        print("\n\n= = = = = = = = =  OBJECT CENTRIC SEARCH = = = = = = = = = \n")
        results = obj_obj_search(request, query_df, card_invariance=request.session['cardinality_invariant'])
    elif request.session['search_type'] == "Location":
        print("\n\n= = = = = = = = =  LOCATION CENTRIC SEARCH = = = = = = = = = \n")
        results = obj_loc_search(request, 
                                 query_df, 
                                 card_invariance=request.session['cardinality_invariant'],
                                 canvas_center=request.session['canvas_center']
                                 )
    else:
        print("UNRECOGNIZED SEARCH TYPE")
        results = None

    return results
    
@api_view(['POST'])
def generate_objects_from_text(request):
    api_key = request.data.get('api_key', '')
    request.session['api_key'] = api_key    
    text_input = request.data.get('text_input', '')
    request.session['query_text'] = text_input
    
    objects_dict = construct_query_from_llm(request)
    request.session['objects_changed'] = True
    response_data = {
        'objects': objects_dict,
        'success': True
    }
    return Response(response_data)

@api_view(['GET'])
def get_search_result(request):
    request.session['objects_changed'] = False
    # Parse search params
    query_dict = json.loads(request.session['object_query'])
    query_df = parse_query_from_dict(query_dict)
    print(query_df)

    results = search(request, query_df)

    # Display results to server terminal for verification
    if not results or len(results) == 0:
        print('No Results Found')
    else:
        print("Found Following Matches to Query:")
        for res in results: 
            print(res)

    # Return respose to UI
    response_data = {
            'locations': results if results else [],
    }
    print(response_data)
    return Response(response_data)

@api_view(['POST'])
def generate_objects_from_image(request):
    request_start = time.time()
    print("[IMAGE_DEBUG] generate_objects_from_image: request received")
    print(f"[IMAGE_DEBUG] generate_objects_from_image: method={request.method}, content_type={request.content_type}")
    print(f"[IMAGE_DEBUG] generate_objects_from_image: FILES keys={list(request.FILES.keys())}")
    print(f"[IMAGE_DEBUG] generate_objects_from_image: DATA keys={list(request.data.keys())}")
    print(f"[IMAGE_DEBUG] generate_objects_from_image: session keys={list(request.session.keys())}")
    print(f"[IMAGE_DEBUG] generate_objects_from_image: cwd={os.getcwd()}")

    api_key = request.data.get('api_key', '')
    print(f"[IMAGE_DEBUG] generate_objects_from_image: api_key present={bool(api_key)}, length={len(api_key) if api_key else 0}")
    if not api_key:
        print("[IMAGE_DEBUG] generate_objects_from_image: ERROR no api_key provided")
        return Response({'error': 'No API key provided'}, status=400)
    request.session['api_key'] = api_key

    if 'image' not in request.FILES:
        print("[IMAGE_DEBUG] generate_objects_from_image: ERROR no image in request.FILES")
        return Response({'error': 'No image provided'}, status=400)

    image = request.FILES['image']
    print(f"[IMAGE_DEBUG] generate_objects_from_image: image name={image.name!r}, size={image.size}, content_type={image.content_type}")

    # Save temporarily
    temp_path = Path("temp_image.png").resolve()
    print(f"[IMAGE_DEBUG] generate_objects_from_image: saving temp image to {temp_path}")
    bytes_written = 0
    with open(temp_path, "wb+") as f:
        for chunk in image.chunks():
            f.write(chunk)
            bytes_written += len(chunk)
    print(f"[IMAGE_DEBUG] generate_objects_from_image: wrote {bytes_written} bytes to {temp_path}, exists={temp_path.exists()}")

    try:
        print("[IMAGE_DEBUG] generate_objects_from_image: starting GoM pipeline")
        gom_start = time.time()
        llm_text = run_gom_and_build_text(temp_path)
        print(f"[IMAGE_DEBUG] generate_objects_from_image: GoM pipeline completed in {time.time() - gom_start:.2f}s")
        print(f"[IMAGE_DEBUG] generate_objects_from_image: llm_text length={len(llm_text)}")
        print(f"[IMAGE_DEBUG] generate_objects_from_image: llm_text preview={llm_text[:500]!r}")

        # Store in session (same as text flow!)
        request.session['query_text'] = llm_text
        print("[IMAGE_DEBUG] generate_objects_from_image: stored llm_text in session")

        # Reuse existing LLM → object pipeline
        print("[IMAGE_DEBUG] generate_objects_from_image: starting construct_query_from_llm")
        llm_pipeline_start = time.time()
        objects_dict = construct_query_from_llm(request)
        print(f"[IMAGE_DEBUG] generate_objects_from_image: construct_query_from_llm completed in {time.time() - llm_pipeline_start:.2f}s")
        print(f"[IMAGE_DEBUG] generate_objects_from_image: final objects_dict={objects_dict}")

        request.session['objects_changed'] = True
        print(f"[IMAGE_DEBUG] generate_objects_from_image: success, total time={time.time() - request_start:.2f}s")
        return Response({
            'objects': objects_dict,
            'llm_text': llm_text,
            'success': True
        })

    except Exception as e:
        print(f"[IMAGE_DEBUG] generate_objects_from_image: EXCEPTION type={type(e).__name__}, message={e!r}")
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

    finally:
        if temp_path.exists():
            temp_path.unlink()
            print(f"[IMAGE_DEBUG] generate_objects_from_image: deleted temp file {temp_path}")

