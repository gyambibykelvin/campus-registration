from django.shortcuts import render, redirect
from .models import Course, Registration, Student, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

import datetime

now = datetime.datetime.now()
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        
        else:
            return render(request, "core/index.html", {"error": "Invalid credentials", 'datetime': now.year})
        
    return render(request, "core/index.html")

def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        level = request.POST.get("level")


        if Student.objects.filter(user__username=username).exists():
            return render(request, "core/signup.html", {"error": "Username already exists"})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
            )
        
        Student.objects.create(
            user=user,
            student_id=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            level=level       
        )

        return redirect("login")

    return render(request, "core/signup.html", {'datetime': now.year})





@login_required
def course(request):
    courses = Course.objects.all()

    student = Student.objects.get(user=request.user)

    registered_courses = Registration.objects.filter(student=student) .values_list('course_id', flat=True)


    context = {
        "courses": courses,
        "registered_courses": registered_courses,
        'datetime': now.year
    }

    return render(request, "core/course_list.html", context)


@login_required
def register_course(request):
    student = Student.objects.get(user=request.user)
    courses = Course.objects.all()

    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course = Course.objects.get(id=course_id)

        Registration.objects.create(
            student=student,
            course=course,
            semester="Second",
            academic_year="2025/2026"
        )

        return redirect("course_list")

    return render(request, "core/register_course.html", {"courses": courses})


@login_required
def dashboard(request):

    student = Student.objects.get(user=request.user)

    registrations = Registration.objects.filter(student=student)

    total_courses = registrations.count()

    total_credits = sum(r.course.credit_hours for r in registrations)

    available_courses = Course.objects.count()

    notifications = []

    max_credits = 17

    if total_courses == 0:
        messages.info(request, "You have not registered any courses yet.")

    if total_credits < 12:
       messages.error(request, "You have not reached the minimum credit hours.")

    if total_credits >= max_credits: 
        messages.error(request, "You have reached the maximum credit hours. You cannot register for more courses.")

   


    remaining_credits = max_credits - total_credits

    now = datetime.datetime.now()
    return render(request,'core/dashboard.html',{
        'student':student,
        'total_courses':total_courses,
        'total_credits':total_credits,
        'available_courses':available_courses,
        'datetime': now.year,
        'notification': notifications

    })

@login_required
def profile(request):

    student = Student.objects.get(user=request.user)

    return render(request, "core/profile.html", {
        "student": student
    })

@login_required
def my_courses(request):
    student = Student.objects.get(user=request.user)

    registrations = Registration.objects.filter(student=student)

    empty = Course.objects.exclude()
    
    if empty == 0:
        return {"empty": "No courses has been registered. Please register to continue"}
    else:
        empty

    return render(request, "core/my_courses.html", {
        "registrations": registrations,
        "empty": empty
    })

@login_required
def drop_course(request, registration_id):

    registration = Registration.objects.get(id=registration_id)

    if registration.student.user == request.user:
        registration.delete()

    return redirect("my_courses")