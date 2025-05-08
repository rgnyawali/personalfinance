from django.urls import path
from .views import SignUpView, logout_then_redirect

app_name='users'
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('logout/', logout_then_redirect, name='logout_then_redirect'),
]