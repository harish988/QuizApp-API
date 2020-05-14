from django.db import models

#Domain Model
class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "Domains"

#Quiz Model
class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    domain_id = models.ForeignKey(Domain, verbose_name = "domain", on_delete=models.CASCADE)
    no_of_questions = models.IntegerField()
    pass_mark = models.IntegerField()
    quiz_image = models.BinaryField(blank=True)
    hardness_choices = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCE', 'Advance'),
    )
    hardness = models.CharField(choices=hardness_choices, default='BEGINNER', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Quizzes"

#Question Model
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=5000)
    question_image = models.BinaryField(blank=True)
    mark = models.IntegerField()
    quiz_type_choices = (
        ('SINGLECHOICE', 'SingleChoice'),
        ('MULTIPLECHOICE', 'MultipleChoice'),
    )
    quiz_type = models.CharField(choices=quiz_type_choices, max_length=20)
    no_of_answers = models.IntegerField()
    correct_answer_id = models.IntegerField()

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name_plural = "Questions"

#Answer Model
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, verbose_name="question", on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)
    answer_image = models.BinaryField(blank=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name_plural = "Answers"