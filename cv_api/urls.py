from django.urls import path
from django.contrib import admin
from face_detector import views as v

urlpatterns = [
    path('face_detection/detect/', v.detect, name='detection response'),
    path('admin/', admin.site.urls),
    path('face_detector/', v.detect),
    path('detector/', v.index),
]
