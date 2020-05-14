from django.db import models
from question.models import Question, Answer, Quiz
from user.models import User


#UserAnswer Model
class UserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, verbose_name="question", on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, verbose_name="answer", on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "User Answers"

#UserScore Model
class UserScore(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "User Scores"