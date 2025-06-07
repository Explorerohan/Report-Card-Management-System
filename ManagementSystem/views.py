from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Student, Teacher, Subject, Result, Announcement
from .forms import (
    UserRegistrationForm, StudentProfileForm, TeacherProfileForm,
    SubjectForm, ResultForm, AnnouncementForm, LoginForm
)

# Creating my views here.
def signup_page(request):
    return render(request, 'signup_page.html')

def stu_signup(request):
    return render(request, 'stu_signup.html')
    
def teach_signup(request):
    return render(request, 'teach_signup.html')

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.role not in allowed_roles:
                    messages.error(request, 'You do not have permission to access this page.')
                    return redirect('dashboard')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found.')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'ManagementSystem/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'user_profile': user_profile,
        'announcements': Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
    }
    
    if user_profile.role == 'teacher':
        context['students'] = Student.objects.all()
        context['results'] = Result.objects.filter(teacher__user_profile=user_profile)
    elif user_profile.role == 'student':
        student = get_object_or_404(Student, user_profile=user_profile)
        context['results'] = Result.objects.filter(student=student)
    
    return render(request, 'ManagementSystem/dashboard.html', context)

@role_required(['admin'])
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            
            # Create user profile
            user_profile = UserProfile.objects.create(
                user=user,
                role=role,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            
            # Create role-specific profile
            if role == 'student':
                Student.objects.create(
                    user_profile=user_profile,
                    roll_number=form.cleaned_data['roll_number'],
                    class_name=form.cleaned_data['class_name'],
                    section=form.cleaned_data['section'],
                    parent_name=form.cleaned_data['parent_name'],
                    parent_phone=form.cleaned_data['parent_phone']
                )
            elif role == 'teacher':
                Teacher.objects.create(
                    user_profile=user_profile,
                    employee_id=form.cleaned_data['employee_id'],
                    subject_specialization=form.cleaned_data['subject_specialization'],
                    qualification=form.cleaned_data['qualification'],
                    experience_years=form.cleaned_data['experience_years']
                )
            
            messages.success(request, f'User registered successfully as {role}.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'ManagementSystem/register.html', {'form': form})

@role_required(['admin'])
def create_student_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user_profile = UserProfile.objects.get(user=user)
            student.save()
            messages.success(request, 'Student profile created successfully.')
            return redirect('dashboard')
    else:
        form = StudentProfileForm()
    return render(request, 'ManagementSystem/create_student_profile.html', {'form': form})

@role_required(['admin'])
def create_teacher_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user_profile = UserProfile.objects.get(user=user)
            teacher.save()
            messages.success(request, 'Teacher profile created successfully.')
            return redirect('dashboard')
    else:
        form = TeacherProfileForm()
    return render(request, 'ManagementSystem/create_teacher_profile.html', {'form': form})

@role_required(['teacher'])
def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.teacher = Teacher.objects.get(user_profile__user=request.user)
            result.save()
            messages.success(request, 'Result added successfully.')
            return redirect('dashboard')
    else:
        form = ResultForm()
    return render(request, 'ManagementSystem/add_result.html', {'form': form})

@role_required(['teacher', 'admin'])
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = UserProfile.objects.get(user=request.user)
            announcement.save()
            messages.success(request, 'Announcement created successfully.')
            return redirect('dashboard')
    else:
        form = AnnouncementForm()
    return render(request, 'ManagementSystem/create_announcement.html', {'form': form})

@login_required
def view_announcements(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'ManagementSystem/announcements.html', {'announcements': announcements})

@role_required(['teacher'])
def view_students(request):
    students = Student.objects.all()
    return render(request, 'ManagementSystem/students.html', {'students': students})

@role_required(['student'])
def view_my_results(request):
    student = get_object_or_404(Student, user_profile__user=request.user)
    results = Result.objects.filter(student=student)
    return render(request, 'ManagementSystem/my_results.html', {'results': results})
