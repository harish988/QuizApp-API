from django.contrib import admin
from .models import Department, Year, Section, User

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

class YearAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department', 'year', 'section']
    list_filter = ['department', 'year', 'section']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(User, UserAdmin)