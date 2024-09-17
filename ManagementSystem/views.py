from django.shortcuts import render,redirect

# Creating my views here.
def signup_page(request):
    return render(request, 'signup_page.html')

def stu_signup(request):
    return render(request, 'stu_signup.html')
    
def teach_signup(request):
    return render(request, 'teach_signup.html')
