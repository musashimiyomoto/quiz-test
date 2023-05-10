from django import forms
from quiz.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']
