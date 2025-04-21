from django.shortcuts import render, redirect
from .models import ProgrammingLanguage, Question, UserAnswer, QuizResult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    languages = ProgrammingLanguage.objects.all()
    return render(request, 'quiz/home.html', {'languages': languages})

@login_required
def quiz_view(request, language_id):
    language = get_object_or_404(ProgrammingLanguage, id=language_id)
    questions = Question.objects.filter(language=language)

    if request.method == 'POST':
        question_id = int(request.POST.get('question_id'))
        selected_option = request.POST.get('option')

        question = get_object_or_404(Question, id=question_id)

        # ✅ Cevaplanmamışsa selected_option None olur
        correct = (selected_option == question.correct_option) if selected_option else False

        UserAnswer.objects.create(
            user=request.user,
            question=question,
            selected_option=selected_option if selected_option else '',
            is_correct=correct
        )

        # ✅ Bir sonraki soruya geç
        next_q = int(request.POST.get('next_q'))
        if next_q < questions.count():
            question = questions[next_q]
            return render(request, 'quiz/quiz.html', {
                'question': question,
                'next_q': next_q + 1,
                'questions': questions,
            })
        else:
            return redirect('result')

    # İlk soru için:
    question = questions[0]
    return render(request, 'quiz/quiz.html', {
        'question': question,
        'next_q': 1,
        'questions': questions,
    })


@login_required
def result_view(request):
    user_answers = UserAnswer.objects.filter(user=request.user).order_by('-id')[:5]
    score = sum(1 for ua in user_answers if ua.is_correct)

    # ✅ Quiz dili nedir? (son cevaplara bakarak)
    if user_answers:
        language = user_answers[0].question.language
        total = len(user_answers)

        # ✅ Skoru kaydet
        QuizResult.objects.create(
            user=request.user,
            language=language,
            score=score,
            total=total
        )

    return render(request, 'quiz/result.html', {'score': score})


@login_required
def history_view(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-date')
    return render(request, 'quiz/history.html', {'results': results})