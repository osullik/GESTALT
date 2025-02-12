
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
import sys
import os
import pickle
import pandas as pd
import json

sys.path.insert(1, os.getcwd()+"/../../code/")
sys.path.insert(1, os.getcwd()+"/../../data/")
sys.path.insert(1, os.path.join(os.getcwd(),"media"))

from OLD_conceptMapping import ConceptMapper
from OLD_search import InvertedIndex

def index(request):
    # Initialize query object data as empty
    request.session['box_data'] = pickle.dumps({}).hex()
    request.session['REGIONS'] = ["Swan Valley, Australia", "Washington D.C., USA", "Hamburg, Germany"]

    return render(request, 'draggable/index.html')

def get_regions(request):
    response_data = {
        'regions': request.session['REGIONS']
    }
    return JsonResponse(response_data)

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

def set_region(request):
    if request.method == 'POST':
        request.session['region'] = request.POST.get('name')
        print("Region selection has been set to.... ", request.session['region'])

        set_data_structure_paths(request)

        response_data = {'success': True}
        return JsonResponse(response_data)

def set_query_text(request):
    if request.method == 'POST':
        request.session['query_text'] = request.POST.get('text_value')
        print("Query text has been set to.... ", request.session['query_text'])

        response_data = {'success': True}
        return JsonResponse(response_data)
    

def get_objects(request):
    # Load data structures using file paths saved in request session
    invertedIndex = InvertedIndex(request.session['INVERTED_INDEX'])
    request.session['VOCAB'] = list(invertedIndex.ii.keys())
    print('VOCAB is:', request.session['VOCAB'])

    response_data = {
        'objects': request.session['VOCAB']
    }
    return JsonResponse(response_data)

def set_search_params(request):
    if request.method == 'POST':
        request.session['object_query'] = request.POST.get('object_query')
        request.session['search_type'] = request.POST.get('search_type')
        request.session['cardinality_invariant'] = (request.POST.get('knows_cardinality') == 'false')
        request.session['canvas_center'] = request.POST.get('canvas_center')

        print("Query was...", request.session['object_query'])
        print("Canvas center is...", request.POST.get('canvas_center'))

        response_data = {'success': True}
        return JsonResponse(response_data)
    
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

def construct_query_from_llm():
    return {"0":{"name":"bus_stop","x":17,"y":433}, 
            "1":{"name":"shed","x":170,"y":644}, 
            "2":{"name":"patio","x":200,"y":133}}

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


def get_pictorial_query(request):
    # Parse search params
    request.session['object_query'] = construct_query_from_llm()
    print(request.session['object_query'])

    # Return respose to UI
    response_data = {
            'object_query': request.session['object_query'],
    }
    print(response_data)
    return JsonResponse(response_data)

    
def get_search_result(request):
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
            'locations': results,
    }
    print(response_data)
    return JsonResponse(response_data)