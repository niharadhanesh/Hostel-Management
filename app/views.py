from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Landing Page
def index(request):
    return render(request, 'index.html')


# Register Page
def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'register.html')


# Login Page
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            # Super Admin Login
            if user.is_superuser:
                messages.success(request, "Admin Login Successful")
                return redirect('admin_dashboard')

            # Normal Student Login
            else:
                messages.success(request, "Student Login Successful")
                return redirect('student_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def student_dashboard(request):
    return render(request, 'student_dashboard.html')

# app/views.py

# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room


# Student List (All Registered Login Users except superuser)
def student_list(request):
    students = User.objects.filter(is_superuser=False)
    return render(request, 'student_list.html', {'students': students})


# Room Page + Add Room
def room_list(request):

    if request.method == "POST":
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        total_beds = request.POST.get('total_beds')
        available_beds = request.POST.get('available_beds')
        rent = request.POST.get('rent')

        Room.objects.create(
            room_number=room_number,
            room_type=room_type,
            total_beds=total_beds,
            available_beds=available_beds,
            rent=rent
        )

        messages.success(request, "Room Added Successfully")
        return redirect('rooms')

    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})