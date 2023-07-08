from django.shortcuts import render

# Create your views here.
from django.conf.urls import include

#def interface(request):
#    return render(request, 'interface.html', {})


import random
import pyautogui
import PIL
from PIL import Image, ImageDraw

import logging
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this



def interface(request):
   if request.method == "POST":
      #ss = pyautogui.screenshot()
      (x, y) = pyautogui.position()
      messages.success(request,'coords have been recorded '+ str(x) + "," + str(y))
      
      img = f'myimg{random.randint(1000,9999)}.png'
      
      return_img = Image.new('RGB', (800, 800), (255, 255, 255))
      d = ImageDraw.Draw(return_img)
      d.text((x, y), str(x) + "," + str(y), fill=(255, 0, 0))
      return_img.convert("L")
      

      
      return_img.save(settings.MEDIA_ROOT/img)
      #messages.success(request,'screenshot has been taken')

      return render(request,'interface.html',{'img':img})
   return render(request,'interface.html')
   
   
#@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation   
def gestalt_init():
    #messages.success(request,'GESTALT setup happening here...')
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)
    logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))

    print(JsonResponse({'mystring':"return this string"}))
    #return render(request,'interface.html')
  
def dummy(var):
	print("testing")
    
def request_page(request):
  if(request.GET.get('mybtn')):
    dummy( int(request.GET.get('mytextbox')) )
    
    fmt = getattr(settings, 'LOG_FORMAT', None)
    lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

    logging.basicConfig(format=fmt, level=lvl)
    logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))
  return render(request,'myApp/templateHTML.html')
  
  
  
def interface2(request):
   if request.method == "POST":
      #ss = pyautogui.screenshot()
      (x, y) = pyautogui.position()
      messages.success(request,'coords have been recorded '+ str(x) + "," + str(y))
      
      img = f'myimg{random.randint(1000,9999)}.png'
      
      return_img = Image.new('RGB', (800, 800), (255, 255, 255))
      d = ImageDraw.Draw(return_img)
      d.text((x, y), str(x) + "," + str(y), fill=(255, 0, 0))
      return_img.convert("L")
      

      
      return_img.save(settings.MEDIA_ROOT/img)
      #messages.success(request,'screenshot has been taken')

      return render(request,'interface.html',{'img':img})
   return render(request,'interface.html')