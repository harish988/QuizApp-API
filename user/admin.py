from django.contrib import admin
from .models import Department, Year, Section, UserProfile

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

class YearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'year', 'section']
    list_filter = ['department', 'year', 'section']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)