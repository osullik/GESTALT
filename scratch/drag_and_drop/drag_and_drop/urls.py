from django.urls import path
from draggable import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coordinates/', views.update_coordinates, name='update_coordinates'),
    path('boxdata/', views.get_box_data, name='get_box_data'),
]
