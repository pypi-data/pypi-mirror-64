from django.urls import path, re_path

from . import views

urlpatterns = [
    path('upload', views.upload),
    re_path('download/(.*)/', views.download),
    path('index/<slug:name>/', views.index),
]
