from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("myfinance:home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Save the user first
        response = super().form_valid(form)
        # Log the user in
        login(self.request, self.object)
        return response
