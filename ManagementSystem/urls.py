from django.urls import path
from .views import signup_page,stu_signup,teach_signup

urlpatterns = [
    path('signup_page',signup_page, name='signup_page'),
    path('student_signup/', stu_signup, name='student_signup'),
    path('teacher_signup/', teach_signup, name='teacher_signup'),
]
