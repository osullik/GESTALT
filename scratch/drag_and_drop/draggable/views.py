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

def prune_invalid_objects(request, objects_dict):
    valid_objects = set(request.session.get('VOCAB', []))

    pruned = {}

    for key, obj in objects_dict.items():
        normalized_name = normalize_object_name(obj["name"])

        # Exact match only. This avoids pruning based on just one different letter.
        if normalized_name in valid_objects:
            pruned[key] = {
                **obj,
                "name": normalized_name
            }
        else:
            print(f"Pruned invalid object: {normalized_name}")

    return pruned

def construct_query_from_llm(request):
    api_key = request.session.get('api_key')
    client = OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")
    query_text = request.session['query_text']

    SYSTEM_PROMPT = "You are tasked with providing coordinates for objects given a textual description of their position. For each object, return coordinates for it where each coordinate ranges from -10 to 10. For orientation, larger y values are North/frontwards. The objects will be together in a large textual description of all of their positions. Respond in the form id: {{id}}\n\nobject name: {{object name}}\n\ncoordinates: (x, y)."
    
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

    raw_result = json.loads(completion.choices[0].message.content)
    print(raw_result)

    
    # TEST = "To the right, there was a bump gate. It was in front of and right of a waterwell, and in front of an anchor, which was left of another waterwell."
    # TEST 2  "In the center was a bus stop. Behind me and to the left was a crossing. In front of me and to the right was a tree."

    res_dict = {}

    for res in raw_result['object_locations']:
        res_dict[str(res['id'])] = {
            "name": res['name'].lower().strip().replace(" ", "_"),
            "x": (res['x'] + 10) * 50,
            "y": (res['y'] + 10) * 50
        }

    res_dict = prune_invalid_objects(request, res_dict)

    print(res_dict)

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
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    image = request.FILES['image']

    # Save temporarily
    temp_path = Path("temp_image.png")
    with open(temp_path, "wb+") as f:
        for chunk in image.chunks():
            f.write(chunk)

    try:
        # Run your GoM pipeline
        llm_text = run_gom_and_build_text(temp_path)

        # Store in session (same as text flow!)
        request.session['query_text'] = llm_text

        # Reuse existing LLM → object pipeline
        objects_dict = construct_query_from_llm(request)
        request.session['objects_changed'] = True
        return Response({
            'objects': objects_dict,
            'llm_text': llm_text,
            'success': True
        })

    except Exception as e:
        return Response({'error': str(e)}, status=500)

    finally:
        if temp_path.exists():
            temp_path.unlink()

