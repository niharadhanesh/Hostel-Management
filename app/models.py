from django.db import models

# Create your models here.
# app/models.py

from django.db import models


class Room(models.Model):
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=50)
    total_beds = models.IntegerField()
    available_beds = models.IntegerField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.room_number


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
# models.py

from django.db import models
from django.contrib.auth.models import User

class RentPayment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    month = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=(
            ('Paid', 'Paid'),
            ('Pending', 'Pending'),
        ),
        default='Pending'
    )
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.username
    
# models.py

from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=(
            ('Pending', 'Pending'),
            ('Resolved', 'Resolved')
        ),
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject