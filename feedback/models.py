from django.db import models
from user.models import User
from question.models import Quiz

#Rating Model
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    site_or_quiz_choices = (
        ('QUIZ', 'Quiz'),
        ('SITE', 'Site'),
    )
    site_or_quiz = models.CharField(choices=site_or_quiz_choices, default='QUIZ', max_length=5)
    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = models.CharField(choices=rating_choices, default='5', max_length=2)
    comments = models.CharField(max_length=5000)
    
    def __str__(self):
        return self.rating

    class Meta:
        verbose_name_plural = "Ratings"