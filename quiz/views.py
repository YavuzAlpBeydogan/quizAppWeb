from django.shortcuts import render, redirect, get_object_or_404
from .models import ProgrammingLanguage, Question, UserAnswer, QuizResult
from django.contrib.auth.decorators import login_required
import uuid  # 👈 buraya ekle
from .models import QuizResult


def home(request):
    languages = ProgrammingLanguage.objects.all()
    return render(request, 'quiz/home.html', {'languages': languages})

@login_required
def quiz_view(request, language_id):
    language = get_object_or_404(ProgrammingLanguage, id=language_id)
    questions = list(Question.objects.filter(language=language).order_by('id'))

    if request.method == 'GET':
        request.session['quiz_session'] = str(uuid.uuid4())

    quiz_session = request.session.get('quiz_session')

    if request.method == 'POST':
        question_id = int(request.POST.get('question_id'))
        selected_option = request.POST.get('option')

        question = get_object_or_404(Question, id=question_id)

        correct = (selected_option.strip().lower() == question.correct_option.strip().lower()) if selected_option else False

        UserAnswer.objects.create(
            user=request.user,
            question=question,
            selected_option=selected_option,
            is_correct=correct,
            quiz_session=quiz_session
        )

        next_q = int(request.POST.get('next_q'))

        if next_q < len(questions):
            next_question = questions[next_q]
            return render(request, 'quiz/quiz.html', {
                'question': next_question,
                'next_q': next_q + 1,
                'question_number': next_q + 1,
                'total_questions': len(questions),
            })
        else:
            return redirect('result')

    question = questions[0]
    return render(request, 'quiz/quiz.html', {
        'question': question,
        'next_q': 1,
        'question_number': 1,
        'total_questions': len(questions),
    })

@login_required
def history_view(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-date')
    return render(request, 'quiz/history.html', {'results': results})

@login_required
def result_view(request):
    quiz_session = request.session.get('quiz_session')

    if not quiz_session:
        return redirect('home')

    user_answers = UserAnswer.objects.filter(
        user=request.user,
        quiz_session=quiz_session
    )

    score = sum(1 for ua in user_answers if ua.is_correct)
    total = user_answers.count()

    if user_answers:
        language = user_answers.first().question.language
        QuizResult.objects.create(
            user=request.user,
            language=language,
            score=score,
            total=total
        )

    return render(request, 'quiz/result.html', {'score': score})
