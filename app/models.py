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