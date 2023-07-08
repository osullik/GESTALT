#from django.urls import path
#from interface import views

#urlpatterns = [
#    path('', views.interface, name='interface'),
#]

from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path('', views.interface),
   path('', views.gestalt_init, name='gestalt_init')
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) #+ static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)