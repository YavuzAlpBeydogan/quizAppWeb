from django.db import models
from django.contrib.auth.models import User

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text[:50]

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)  # Bu satır önemli
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.id}"
    
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.language.name} - {self.score}/{self.total}"
    