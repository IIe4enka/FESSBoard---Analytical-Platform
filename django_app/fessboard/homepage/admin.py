from django.contrib import admin
from .models import *

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['student_name','student_midname', 'student_surname', 'bachelors_start_year', 'masters_start_year']
    pass

class TeacherAdmin(admin.ModelAdmin):
    search_fields = ['teacher_name','teacher_midname', 'teacher_surname', 'teacher_university']
    pass

class UniversityAdmin(admin.ModelAdmin):
    search_fields = ['university_name','university_region']
    pass

admin.site.register(Students, StudentAdmin)
admin.site.register(Teachers, TeacherAdmin)
admin.site.register(Universities, UniversityAdmin)

