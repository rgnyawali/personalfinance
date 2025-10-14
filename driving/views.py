from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View


# Create your views here.

def homeview(request):
	return render(request, 'driving/home.html',{})
