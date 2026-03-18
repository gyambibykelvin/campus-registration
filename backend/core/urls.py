from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.course, name="course_list"),
    path("register/", views.register_course, name="register_course"),
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("my-courses/", views.my_courses, name="my_courses"),
    path("drop-course/<int:registration_id>/", views.drop_course, name= "drop_course")
]