from django.contrib import admin
from .models import User, Staff, Student, Device, Attendance, Parent, Class, Notification

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Device)
admin.site.register(Attendance)
admin.site.register(Parent)
admin.site.register(Class)
admin.site.register(Notification)