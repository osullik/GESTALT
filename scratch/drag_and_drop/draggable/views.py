from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'draggable/index.html')

def get_coordinates(request):
    if request.method == 'POST':
        x = request.POST.get('x')
        y = request.POST.get('y')
        return JsonResponse({'x': x, 'y': y})
    return JsonResponse({'error': 'Invalid request method'})
