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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def student_list(request):
    students = User.objects.filter(is_superuser=False, is_staff=False)

    # Update student from modal
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student = get_object_or_404(User, id=student_id)

        student.first_name = request.POST.get("first_name")
        student.username = request.POST.get("username")
        student.email = request.POST.get("email")
        student.save()

        return redirect('student_list')

    return render(request, 'student_list.html', {'students': students})


def delete_student(request, id):
    student = get_object_or_404(User, id=id)
    student.delete()
    return redirect('student_list')


# views.py
# views.py
from .models import Student
from django.shortcuts import render, redirect, get_object_or_404
# views.py  (FULL FIXED)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room
# views.py  (REPLACE room_list FULLY)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room


def room_list(request):

    # ---------------- POST ----------------
    if request.method == "POST":

        action = request.POST.get("action")

        # -------- ADD ROOM --------
        if action == "room":

            Room.objects.create(
                room_number=request.POST.get("room_number"),
                room_type=request.POST.get("room_type"),
                total_beds=request.POST.get("total_beds"),
                available_beds=request.POST.get("available_beds"),
                rent=request.POST.get("rent")
            )

            messages.success(request, "Room Added Successfully")

        # -------- ASSIGN ROOM --------
        elif action == "assign":

            student_id = request.POST.get("student_id")
            room_id = request.POST.get("assign_room_id")

            student = get_object_or_404(User, id=student_id)
            room = get_object_or_404(Room, id=room_id)

            if room.available_beds > 0:

                # store room id in last_name
                student.last_name = str(room.id)
                student.save()

                room.available_beds -= 1
                room.save()

                messages.success(request, "Room Assigned Successfully")

            else:
                messages.error(request, "No Beds Available")

        return redirect("rooms")

    # ---------------- GET ----------------
    rooms = Room.objects.all()

    students = User.objects.filter(
        is_superuser=False,
        is_staff=False
    )

    return render(request, "room_list.html", {
        "rooms": rooms,
        "students": students
    })

def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect("rooms")

# views.py

from django.shortcuts import render

# My Room Page
def my_room(request):
    student = request.user

    # Example: linked room from student profile
    room = getattr(student, 'room', None)

    return render(request, 'my_room.html', {'room': room})

# views.py

# views.py  (STUDENT RENT STATUS PAGE)

from django.shortcuts import render
from .models import Room


def rent_status(request):

    student = request.user
    room = None
    notified = False
    status = "Pending"
    paid_date = ""

    if student.last_name:
        try:
            room = Room.objects.get(id=int(student.last_name))
        except:
            room = None

    if "NOTIFY|" in student.first_name:
        notified = True

    if "PAID|" in student.first_name:
        status = "Paid"
        paid_date = student.first_name.split("PAID|")[1]

    amount = room.rent if room else 0
    paid = amount if status == "Paid" else 0
    balance = 0 if status == "Paid" else amount

    rent_history = [{
        "month": "Current Month",
        "amount": amount,
        "paid": paid,
        "balance": balance,
        "status": status,
        "paid_date": paid_date
    }]

    return render(request, "rent_status.html", {
        "room": room,
        "rent_history": rent_history,
        "notified": notified
    })
# views.py


# views.py  (ADMIN RENT PAGE)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import now
from .models import Room


def rent_list(request):

    if request.method == "POST":

        student_id = request.POST.get("student_id")
        action = request.POST.get("action")

        student = User.objects.get(id=student_id)

        # PAYMENT DONE
        if action == "paid":
            student.first_name = "PAID|" + str(now().date())
            student.save()
            messages.success(request, "Payment marked as done")

        # NOTIFY STUDENT
        elif action == "notify":
            student.first_name = "NOTIFY|" + student.first_name
            student.save()
            messages.success(request, f"Reminder sent to {student.username}")

        return redirect("rent")

    students = User.objects.filter(
        is_superuser=False,
        is_staff=False
    )

    rent_data = []

    for student in students:

        room = None
        status = "Pending"
        paid_date = ""

        if student.last_name:
            try:
                room = Room.objects.get(id=int(student.last_name))
            except:
                room = None

        if "PAID|" in student.first_name:
            status = "Paid"
            paid_date = student.first_name.split("PAID|")[1]

        rent_data.append({
            "student": student,
            "room": room,
            "status": status,
            "paid_date": paid_date
        })

    return render(request, "rent.html", {
        "rent_data": rent_data
    })
    
# views.py

from .models import Complaint
from django.contrib import messages

def student_complaints(request):

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        Complaint.objects.create(
            student=request.user,
            subject=subject,
            message=message
        )

        messages.success(request, "Complaint submitted successfully")
        return redirect('student_complaints')

    complaints = Complaint.objects.filter(
        student=request.user
    ).order_by('-id')

    return render(request, "student_complaints.html", {
        "complaints": complaints
    })
    
# views.py

from .models import Complaint
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


def admin_complaints(request):

    # -------- RESOLVE ACTION --------
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")

        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = "Resolved"
        complaint.save()

        messages.success(request, "Complaint marked as resolved")
        return redirect('admin_complaints')

    # -------- GET ALL COMPLAINTS --------
    complaints = Complaint.objects.all().order_by('-id')

    return render(request, "admin_complaints.html", {
        "complaints": complaints
    })