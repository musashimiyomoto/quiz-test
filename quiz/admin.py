from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from quiz.models import (Quiz,
                         Question,
                         Choice)


class ChoiceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_correct'):
                correct_count += 1
        if correct_count == 0:
            raise ValidationError('At least one choice must be marked as correct.')
        if correct_count == len(self.forms):
            raise ValidationError('All choices cannot be marked as correct.')


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    min_num = 2
    formset = ChoiceInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    min_num = 1
    inlines = [ChoiceInline]


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
