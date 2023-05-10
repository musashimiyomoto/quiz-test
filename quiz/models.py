from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=256)
    category = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=512)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def get_next_question(self):
        next_question = Question.objects.filter(quiz=self.quiz, pk__gt=self.pk).first()
        return next_question

    def __str__(self):
        return self.text


class Choice(models.Model):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class QuizTaker(models.Model):
    completed = models.BooleanField(default=False)
    correct_answers = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title}'
