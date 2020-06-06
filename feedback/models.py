from django.db import models
from user.models import UserProfile
from question.models import Quiz

#Rating Model
class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, verbose_name="user", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    site_or_quiz_choices = (
        ('QUIZ', 'Quiz'),
        ('SITE', 'Site'),
    )
    site_or_quiz = models.CharField(choices=site_or_quiz_choices, default='Quiz', max_length=5)
    rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = models.IntegerField(choices=rating_choices, default=5)
    comments = models.CharField(max_length=2000, null=True)
    
    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name_plural = "Ratings"
        managed = True
        db_table = 'rating'
