from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)
from django.contrib.auth.decorators import login_required

from quiz.models import (Quiz,
                         Question,
                         Choice,
                         QuizTaker)


def index(request):
    quizzes = Quiz.objects.all()

    context = {'quizzes': quizzes, 'categories': list(set([quiz.category for quiz in quizzes]))}

    return render(request=request, template_name='quiz/index.html', context=context)


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_taker, created = QuizTaker.objects.get_or_create(user=request.user, quiz=quiz)

    if quiz_taker.completed:
        return redirect(to='quiz:result', quiz_id=quiz_id)

    if quiz_taker.current_question:
        return redirect(to='quiz:question', quiz_id=quiz_id, question_id=quiz_taker.current_question.pk)
    else:
        first_question = quiz.question_set.first()
        if first_question:
            quiz_taker.current_question = first_question
            quiz_taker.save()
            return redirect(to='quiz:question', quiz_id=quiz_id, question_id=first_question.pk)
        else:
            return redirect(to='quiz:result', quiz_id=quiz_id)


@login_required
def question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id)
    quiz_taker = get_object_or_404(QuizTaker, user=request.user, quiz=quiz)

    if request.method == 'POST':
        selected_choices = request.POST.getlist('choice[]')
        if len(selected_choices) > 0:
            is_correct = True
            for selected_choice in selected_choices:
                choice = get_object_or_404(Choice, pk=selected_choice)
                if not choice.is_correct:
                    is_correct = False

            next_question = question.get_next_question()
            quiz_taker.current_question = next_question

            if is_correct:
                quiz_taker.correct_answers += 1

            quiz_taker.save()

            if next_question:
                return redirect('quiz:question', quiz_id=quiz_id, question_id=next_question.pk)
            else:
                quiz_taker.completed = True
                quiz_taker.save()
                return redirect('quiz:result', quiz_id=quiz_id)

    if question != quiz_taker.current_question:
        if quiz_taker.current_question:
            return redirect('quiz:question', quiz_id=quiz_id, question_id=quiz_taker.current_question.pk)
        else:
            return redirect('quiz:start', quiz_id=quiz_id)

    context = {'quiz': quiz, 'question': question}

    return render(request=request, template_name='quiz/question.html', context=context)


@login_required
def result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_taker = get_object_or_404(QuizTaker, user=request.user, quiz=quiz)

    correct_answers = quiz_taker.correct_answers
    total_questions = quiz.question_set.count()
    percentage = (correct_answers / total_questions) * 100

    context = {
        'quiz': quiz,
        'correct_answers': correct_answers,
        'not_correct_answers': total_questions - correct_answers,
        'percentage': percentage
    }

    return render(request=request, template_name='quiz/result.html', context=context)
