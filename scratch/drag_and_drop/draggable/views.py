
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

box_data = {}  # List to store the box data
base_dir = settings.MEDIA_ROOT 
conceptMaps = None
invertedIndex = None
referenceLocations = None
   

# def index(request):
#     return render(request, 'draggable/index.html')

# def update_coordinates(request):
#     if request.method == 'POST':
#         index = request.POST.get('index')
#         name = request.POST.get('name')
#         x = request.POST.get('x')
#         y = request.POST.get('y')
#         box_data[index]={"name":name, "x": int(x), "y": int(y)}  # Store box data as a tuple
#         response_data = {
#             'index': index,
#             'x': x,
#             'y': y
#         }
#         return JsonResponse(response_data)

def get_box_data(request):
    response_data = {
        'box_data': box_data
    }
    print(response_data)
    return JsonResponse(response_data)
    
def get_objects(request):
    response_data = {
        'objects': ['pond','testnm']
    }
    print("VIEWS SAYS: ", response_data)
    return JsonResponse(response_data)

def index(request):
    print("STARTUP....")
    dataDirectory = ""
    for p in sys.path:
        if p.endswith("media"):
           dataDirectory = p 

    assert (dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory - does it exist?"
    
    CONCEPT_MAPS = os.path.join(dataDirectory,'data', 'SV', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
    INVERTED_INDEX = os.path.join(dataDirectory,'data', 'SV', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
    UI_LOCATIONS = os.path.join(dataDirectory,'data', 'SV', 'output', 'concept_mapping', 'RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON')
    
    invertedIndex = InvertedIndex(INVERTED_INDEX)
    VOCAB = invertedIndex.ii.keys()
    print('VOCAB is:', VOCAB)
  
    with open(CONCEPT_MAPS, "rb") as inFile:
        global conceptMaps
        conceptMaps = pickle.load(inFile)
    CM = ConceptMapper()

    with open(UI_LOCATIONS, "r") as inFile:
        global referenceLocations
        referenceLocations = json.load(inFile)
        
    return render(request, 'draggable/index.html')

def update_coordinates(request):
    if request.method == 'POST':
        index = request.POST.get('index')
        name = request.POST.get('name')
        x = request.POST.get('x')
        y = request.POST.get('y')
        box_data[index]={"name":name, "x": int(x), "y": int(y)}  # Store box data as a tuple
        response_data = {
            'index': index,
            'x': x,
            'y': y
        }
        return JsonResponse(response_data)
        
@csrf_exempt         
def get_search_result(request):
    print("About to search for: ", box_data['0'])

    # Do the search with everything in box_data  
    flatDict = {}
    flatDict["name"] = []
    flatDict["longitude"] = []
    flatDict["latitude"] = []
    flatDict["predicted_location"] = []
    for key in box_data.keys():
        print("KEY: ", box_data[key]["name"], box_data[key]["x"], box_data[key]["y"])
        flatDict["name"].append("palm_tree")#box_data[key]["name"])
        flatDict["longitude"].append(box_data[key]["x"])
        flatDict["latitude"].append(box_data[key]["y"])
        flatDict["predicted_location"].append("PICTORIAL_QUERY")
    
    query_df = pd.DataFrame.from_dict(flatDict, orient='columns')
    print(query_df)
    
    print("\n\n= = = = = = = = =  OBJECT CENTRIC SEARCH = = = = = = = = = \n")
    CM = ConceptMapper()
    queryMap = CM.createConceptMap(input_df=query_df, inputFile=None)
    searchOrder = CM.getSearchOrder(queryMap['PICTORIAL_QUERY'])
    print(searchOrder)
    
    results = []
    for locationCM in conceptMaps.keys():
        result = CM.searchMatrix(conceptMaps[locationCM],searchOrder.copy())
        if result == True: 
            results.append(locationCM)
            result = False
            
    if len(results) == 0:
        print('No Results Found')
    else:
        print("Found Following Matches to Query:")
        for res in results: 
            print(res)
                    
                    

    response_data = {
            'locations': results,
        }
    print(response_data)
    
    return JsonResponse(response_data)

#  Was originally using this code to access the separate html file:
# def get_box_data2(request):
#     response_data = {
#         'box_data': box_data
#     }
#     print(response_data)
#     return JsonResponse(response_data)

# def index2(request):
#     return render(request, 'draggable/index2.html')

# def update_coordinates2(request):
#     if request.method == 'POST':
#         index2 = request.POST.get('index2')
#         name = request.POST.get('name')
#         x = request.POST.get('x')
#         y = request.POST.get('y')
#         box_data[index2]={"name":name, "x": int(x), "y": int(y)}  # Store box data as a tuple
#         response_data = {
#             'index2': index2,
#             'x': x,
#             'y': y
#         }
#         return JsonResponse(response_data)