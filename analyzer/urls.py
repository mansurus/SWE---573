from django.urls import path
from . import views

urlpatterns = [
    path('analyzer', views.nltkView, name="analyzer"),    
]