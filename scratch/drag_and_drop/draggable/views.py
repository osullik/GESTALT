
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

from conceptMapping import ConceptMapper
from search import InvertedIndex

base_dir = settings.MEDIA_ROOT 


def get_box_data(request):
    response_data = {
        'box_data': request.session['box_data']
    }
    print(response_data)
    return JsonResponse(response_data)
    
def get_objects(request):
    response_data = {
        'objects': request.session['VOCAB'] #['pond','tree']
    }
    return JsonResponse(response_data)

def index(request):
    # Initialize query object data as empty
    request.session['box_data'] = pickle.dumps({}).hex()

    return render(request, 'draggable/index.html')

def update_coordinates(request):
    if request.method == 'POST':
        index = request.POST.get('index')
        name = request.POST.get('name')
        x = request.POST.get('x')
        y = request.POST.get('y')

        # Load, update, and repickle the box_data dict
        box_data = pickle.loads(bytes.fromhex(request.session['box_data']))
        box_data[index] = {"name": name, "x": int(x), "y": int(y)}
        request.session['box_data'] = pickle.dumps(box_data).hex()

        response_data = {
            'index': index,
            'x': x,
            'y': y
        }
        return JsonResponse(response_data)
        
def set_region(request):
    if request.method == 'POST':
        request.session['region'] = request.POST.get('name')
        
        dataDirectory = ""
        for p in sys.path:
            if p.endswith("media"):
               dataDirectory = p 

        assert (dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory"
        
        # Set data file paths based on region choice
        if request.session['region'] == "Swan Valley, Australia":
            print("GOT SV.............")
            request.session['CONCEPT_MAPS_PATH'] = os.path.join(dataDirectory,'data', 'SV', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
            request.session['INVERTED_INDEX'] = os.path.join(dataDirectory,'data', 'SV', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
            request.session['LOCATION_STRUCTURE_PATH'] = os.path.join(dataDirectory,'data', 'SV', 'output', 'concept_mapping', 'RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON')
        elif request.session['region'] == "Washington D.C.":
            print("GOT DC.............")
            print("DC functionality not implemented yet......")
        else:
            print("UNRECOGNIZED REGION SELECTED")

        # Load data structures using file paths set above
        invertedIndex = InvertedIndex(request.session['INVERTED_INDEX'])
        request.session['VOCAB'] = list(invertedIndex.ii.keys())
        print('VOCAB is:', request.session['VOCAB'])
  
        response_data = {'success': True}
        return JsonResponse(response_data)
    
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
        result = CM.searchMatrix(conceptMaps[locationCM], searchOrder.copy())
        if result == True: 
            results.append(locationCM)
            result = False

    return results

def obj_loc_search(request, query_df, card_invariance):
        #with open(request.session['LOCATION_STRUCTURE_PATH'], "r") as inFile:
        #    referenceLocations = json.load(inFile)
    return None

def set_search_params(request):
    request.session['search_type'] = request.POST.get('search_type')
    request.session['cardinality_invariant'] = (request.POST.get('knows_cardinality') == 'false')
    response_data = {'success': True}
    return JsonResponse(response_data)
              
def get_search_result(request):
    box_data = box_data = pickle.loads(bytes.fromhex(request.session['box_data']))
    print("About to search for: ", box_data)

    # Create query dataframe from everything in box_data  
    flatDict = {"name":[], "longitude":[], "latitude":[], "predicted_location":[]}

    for key in box_data.keys():
        flatDict["name"].append(box_data[key]["name"])
        flatDict["longitude"].append(box_data[key]["x"])
        flatDict["latitude"].append(box_data[key]["y"])
        flatDict["predicted_location"].append("PICTORIAL_QUERY")
    
    query_df = pd.DataFrame.from_dict(flatDict, orient='columns')
    print(query_df)
    
    # Do the search  
    print("SEARCH TYPE IS: ", request.session['search_type'])
    print("CARDINALITY INVARIANT: ", request.session['cardinality_invariant'])

    if request.session['search_type'] == "Object":
        print("\n\n= = = = = = = = =  OBJECT CENTRIC SEARCH = = = = = = = = = \n")
        results = obj_obj_search(request, query_df, card_invariance=request.session['cardinality_invariant'])
    elif request.session['search_type'] == "Location":
        print("\n\n= = = = = = = = =  LOCATION CENTRIC SEARCH = = = = = = = = = \n")
        results = obj_loc_search(request, query_df, card_invariance=request.session['cardinality_invariant'])
    else:
        print("UNRECOGNIZED SEARCH TYPE")
        results = None

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