from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Student, Teacher, Subject, Result, Announcement

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleRoleFields()'}),
        help_text='Select whether this user is a student or teacher'
    )
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    # Student-specific fields
    roll_number = forms.CharField(max_length=20, required=False)
    class_name = forms.CharField(max_length=10, required=False)
    section = forms.CharField(max_length=5, required=False)
    parent_name = forms.CharField(max_length=100, required=False)
    parent_phone = forms.CharField(max_length=15, required=False)

    # Teacher-specific fields
    employee_id = forms.CharField(max_length=20, required=False)
    subject_specialization = forms.CharField(max_length=100, required=False)
    qualification = forms.CharField(max_length=100, required=False)
    experience_years = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'student':
            # Validate student-specific fields
            if not cleaned_data.get('roll_number'):
                self.add_error('roll_number', 'Roll number is required for students')
            if not cleaned_data.get('class_name'):
                self.add_error('class_name', 'Class is required for students')
            if not cleaned_data.get('section'):
                self.add_error('section', 'Section is required for students')
            if not cleaned_data.get('parent_name'):
                self.add_error('parent_name', 'Parent name is required for students')
            if not cleaned_data.get('parent_phone'):
                self.add_error('parent_phone', 'Parent phone is required for students')
        
        elif role == 'teacher':
            # Validate teacher-specific fields
            if not cleaned_data.get('employee_id'):
                self.add_error('employee_id', 'Employee ID is required for teachers')
            if not cleaned_data.get('subject_specialization'):
                self.add_error('subject_specialization', 'Subject specialization is required for teachers')
            if not cleaned_data.get('qualification'):
                self.add_error('qualification', 'Qualification is required for teachers')
            if not cleaned_data.get('experience_years'):
                self.add_error('experience_years', 'Experience years is required for teachers')
        
        return cleaned_data

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_number', 'class_name', 'section', 'date_of_birth', 'parent_name', 'parent_phone')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('employee_id', 'subject_specialization', 'qualification', 'experience_years')

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'code', 'description')

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('student', 'subject', 'marks_obtained', 'total_marks', 'grade', 'remarks')
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3})
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput) 