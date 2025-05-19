from django.contrib import admin
from .models import User, Staff, Student, Device, Attendance, Parent, ClassGroup, Notification, School, Department

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Device)
admin.site.register(Attendance)
admin.site.register(Parent)
admin.site.register(ClassGroup)
admin.site.register(Notification)
admin.site.register(School)
admin.site.register(Department)
