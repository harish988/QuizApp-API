from django.contrib import admin
from .models import UserAnswer, UserScore

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'quiz_id', 'question_id', 'answer_id']
    list_filter = ['user_id', 'quiz_id', 'question_id', 'answer_id']

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'quiz_id', 'score']
    list_filter = ['user_id', 'quiz_id', 'score']

admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(UserScore, UserScoreAdmin)