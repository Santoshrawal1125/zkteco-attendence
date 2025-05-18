from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


# User model: extended for roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# Class model (school/class group)
class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Student model linked to User and Class
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    device_user_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  # added

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.enrollment_number}"


# Parent model linked to User and related Students
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return self.user.get_full_name()


# Staff model linked to User
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    device_user_id = models.CharField(max_length=50, unique=True, null=True, blank=True)  # added

    def __str__(self):
        return self.user.get_full_name()


# Device model representing ZKTeco devices
class Device(models.Model):
    device_name = models.CharField(max_length=100)
    device_ip = models.GenericIPAddressField()
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.device_name} ({self.serial_number})"


# Notification model (for sending alerts or info)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.user.username} at {self.timestamp}"


# Attendance model for both students and staff

class Attendance(models.Model):
    ATTENDANCE_TYPE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    attendance_type = models.CharField(max_length=20, choices=ATTENDANCE_TYPE_CHOICES)
    verify_mode = models.CharField(max_length=20, blank=True, null=True)  # fingerprint or face
    check_type = models.CharField(max_length=20, blank=True, null=True)  # e.g. in/out

    def clean(self):
        if not self.student and not self.staff:
            raise ValidationError('Attendance must be linked to either a student or staff.')

    def __str__(self):
        if self.student:
            return f"Attendance for student {self.student} on {self.timestamp}"
        elif self.staff:
            return f"Attendance for staff {self.staff} on {self.timestamp}"
        else:
            return f"Attendance record on {self.timestamp} (no user linked)"
