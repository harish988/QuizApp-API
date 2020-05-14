from django.contrib import admin
from .models import Quiz, Question, Domain, Answer

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain_id', 'no_of_questions', 'pass_mark', 'hardness']
    list_filter = ['domain_id', 'hardness']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz_id', 'mark', 'quiz_type', 'correct_answer_id']
    list_filter = ['quiz_id', 'quiz_type']

class DomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_id', 'question_id', 'answer_text']
    list_filter = ['quiz_id', 'question_id']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Answer, AnswerAdmin)