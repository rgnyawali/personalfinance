from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.indexview, name='home'),
]