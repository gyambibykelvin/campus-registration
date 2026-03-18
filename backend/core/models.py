from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class Course(models.Model):
    course_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    credit_hours = models.IntegerField()
    semester = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=9)
    max_enrollments = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_code} - {self.title}"
    
class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)

    class Meta:
        unique_together = ('student', 'course', 'semester', 'academic_year')

    def __str__(self):
        return f"{self.student} - {self.course}"
    

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('dropped', 'Dropped'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered'
    )

    grade = models.CharField(max_length=3, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')

class Result(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    score = models.FloatField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.registration.student} - {self.grade}"