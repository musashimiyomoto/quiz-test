from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('start/<int:quiz_id>/', views.start_quiz, name='start'),
    path('question/<int:quiz_id>/<int:question_id>/', views.question, name='question'),
    path('result/<int:quiz_id>/', views.result, name='result')
]
