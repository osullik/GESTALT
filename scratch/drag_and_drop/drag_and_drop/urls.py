from django.urls import path
from draggable import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('coordinates/', views.update_coordinates, name='update_coordinates'),
    path('boxdata/', views.get_box_data, name='get_box_data'),
    path('searchresult/', views.get_search_result, name='get_search_result'),
    path('getobjs/', views.get_objects, name='get_objects'),
    path('setregion/', views.set_region, name='set_region'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# Was originally using this code to access the separate html file:
# urlpatterns = [
#     path('', views.index2, name='index2'),
#     path('coordinates/', views.update_coordinates2, name='update_coordinates2'),
#     path('boxdata/', views.get_box_data2, name='get_box_data2'),
# ]
