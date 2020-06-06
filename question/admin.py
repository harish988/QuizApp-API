from django.contrib import admin
from .models import Quiz, Question, Domain, Answer

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain_id', 'no_of_questions', 'pass_mark', 'hardness']
    list_filter = ['domain_id', 'hardness']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz_id', 'mark', 'question_type']
    list_filter = ['quiz_id', 'question_type']

class DomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_id', 'answer_text', 'is_correct_answer']
    list_filter = ['quiz_id', 'is_correct_answer']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Answer, AnswerAdmin)