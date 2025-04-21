from django.contrib import admin
from .models import ProgrammingLanguage, Question, UserAnswer
from .models import QuizResult

admin.site.register(QuizResult)
admin.site.register(ProgrammingLanguage)
admin.site.register(Question)
admin.site.register(UserAnswer)
