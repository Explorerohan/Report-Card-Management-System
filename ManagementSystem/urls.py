from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('create-student-profile/<int:user_id>/', views.create_student_profile, name='create_student_profile'),
    path('create-teacher-profile/<int:user_id>/', views.create_teacher_profile, name='create_teacher_profile'),
    path('add-result/', views.add_result, name='add_result'),
    path('create-announcement/', views.create_announcement, name='create_announcement'),
    path('announcements/', views.view_announcements, name='announcements'),
    path('students/', views.view_students, name='students'),
    path('my-results/', views.view_my_results, name='my_results'),
]
