
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

def index(request):
    # Initialize query object data as empty
    request.session['box_data'] = pickle.dumps({}).hex()
    request.session['REGIONS'] = ["Swan Valley, Australia", "Washington D.C."]

    return render(request, 'draggable/index.html')

def get_regions(request):
    response_data = {
        'regions': request.session['REGIONS']
    }
    return JsonResponse(response_data)


def set_region(request):
    if request.method == 'POST':
        request.session['region'] = request.POST.get('name')
        print("Region selection has been set to.... ", request.session['region'])

        response_data = {'success': True}
        return JsonResponse(response_data)
    

def get_objects(request):
    response_data = {
        'objects': ['tmp']#request.session['VOCAB']
    }
    return JsonResponse(response_data)

def set_search_params(request):
    if request.method == 'POST':
        #request.session['object_query'] = request.POST.get('object_query')
        request.session['search_type'] = request.POST.get('search_type')
        request.session['cardinality_invariant'] = (request.POST.get('knows_cardinality') == 'false')
        response_data = {'success': True}
        print("Query was...", request.POST.get('object_query'))
        return JsonResponse(response_data)