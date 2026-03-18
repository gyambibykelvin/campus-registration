from django.contrib import admin
from .models import User, Course, Enrollment, Result, Student, Registration

# Register your models here.

class student(admin.ModelAdmin):
    list_display = ("id", "student_id", "first_name", "last_name", "email", "level")

class course(admin.ModelAdmin):
    list_display = ("id", "course_code", "title", "credit_hours", "semester", "academic_year", "max_enrollments")

class result(admin.ModelAdmin):
    list_display = ("id", "registration", "score", "grade" )

class registration(admin.ModelAdmin):
    list_display = ("student", "course", "semester", "academic_year")

class user(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "password", "date_joined", "last_login", "role")

admin.site.register(User, user)
admin.site.register(Course, course)
admin.site.register(Enrollment)
admin.site.register(Result, result)
admin.site.register(Student, student)
admin.site.register(Registration, registration)