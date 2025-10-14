from django.urls import path, include
from . import views

app_name = 'driving'

urlpatterns = [
    path('', views.homeview, name='home'),
]