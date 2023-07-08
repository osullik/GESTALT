from django.urls import path
from draggable import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coordinates/', views.get_coordinates, name='get_coordinates'),
]
