from django.urls import path
from draggable import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coordinates/', views.update_coordinates, name='update_coordinates'),
    path('boxdata/', views.get_box_data, name='get_box_data'),
]

# Was originally using this code to access the separate html file:
# urlpatterns = [
#     path('', views.index2, name='index2'),
#     path('coordinates/', views.update_coordinates2, name='update_coordinates2'),
#     path('boxdata/', views.get_box_data2, name='get_box_data2'),
# ]
