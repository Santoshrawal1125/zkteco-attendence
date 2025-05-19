from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


# Custom User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('staff', 'Staff'),
        ('school_admin', 'School Admin'),
        ('superadmin', 'SuperAdmin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# School model
class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school_admin')
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Class model (school/class group)
class ClassGroup(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.school.name}"


class Department(models.Model):
    dept_name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.dept_name


# Staff model
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    staff_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    device_user_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student_class = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    device_user_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.enrollment_number}"


# Parent model
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    children = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return self.user.get_full_name()


# Device model (ZKTeco devices)
class Device(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    device_ip = models.GenericIPAddressField()
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.device_name} ({self.serial_number})"


# Notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.user.username} at {self.timestamp}"


# Attendance model
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
    check_type = models.CharField(max_length=20, blank=True, null=True)  # in/out

    def clean(self):
        if not self.student and not self.staff:
            raise ValidationError('Attendance must be linked to either a student or staff.')

    def __str__(self):
        if self.student:
            return f"Attendance for student {self.student} on {self.timestamp}"
        elif self.staff:
            return f"Attendance for staff {self.staff} on {self.timestamp}"
        else:
            return f"Attendance on {self.timestamp}"
