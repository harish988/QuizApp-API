from django.contrib import admin
from .models import Rating

class RatingAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'quiz_id', 'site_or_quiz', 'rating']
    list_filter = ['site_or_quiz', 'rating']

admin.site.register(Rating, RatingAdmin)