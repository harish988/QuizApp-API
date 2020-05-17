from django.db import models

#Domain Model
class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "Domains"
        managed = True
        db_table = 'domain'

#Quiz Model
class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    domain_id = models.ForeignKey(Domain, verbose_name = "domain", on_delete=models.CASCADE)
    no_of_questions = models.IntegerField()
    no_of_question_to_display = models.IntegerField()
    pass_mark = models.IntegerField()
    total_marks = models.IntegerField()
    time_in_minutes = models.IntegerField()
    quiz_image = models.BinaryField(blank=True)
    hardness_choices = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCE', 'Advance'),
    )
    hardness = models.CharField(choices=hardness_choices, default='BEGINNER', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Quizzes"
        managed = True
        db_table = 'quiz'

#Question Model
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=5000)
    question_image = models.BinaryField(blank=True)
    mark = models.IntegerField()
    question_type_choices = (
        ('SINGLECHOICE', 'SingleChoice'),
        ('MULTIPLECHOICE', 'MultipleChoice'),
        ('TEXT', 'Text'),
    )
    question_type = models.CharField(choices=question_type_choices, max_length=20)
    no_of_answers = models.IntegerField()

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name_plural = "Questions"
        managed = True
        db_table = 'question'

#Answer Model
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, verbose_name="quiz", on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, verbose_name="question", on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)
    answer_image = models.BinaryField(blank=True)
    is_correct_answer_choices = (
        ('TRUE', 'True'),
        ('FALSE', 'False'),
    )
    is_correct_answer = models.CharField(choices=is_correct_answer_choices, max_length=10)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name_plural = "Answers"
        managed = True
        db_table = 'answer'