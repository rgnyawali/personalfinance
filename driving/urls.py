from django.urls import path, include
from . import views

app_name = 'driving'

urlpatterns = [
    path('', views.homeview, name='home'),
    path('quiz/', views.QuizView.as_view(), name='quiz_start'),
    path('quiz/<int:question_id>/', views.QuizView.as_view(), name='quiz_question'),
    path('quiz/complete/', views.QuizCompleteView.as_view(), name='quiz_complete'),
    path('addq/', views.add_question, name='add_question'),
]