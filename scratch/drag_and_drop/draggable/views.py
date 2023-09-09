
from django.shortcuts import render
from django.http import JsonResponse

box_data = {}  # List to store the box data

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

def index(request):
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