from rest_framework import serializers
from .models import Staff, User, Department, School, SchoolAdmin, StudentClass, Student, Attendance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class StaffSerializers(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = "__all__"


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class SchoolAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolAdmin
        fields = ['id']


class SchoolSerializers(serializers.ModelSerializer):
    school_admin = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = "__all__"

    def get_school_admin(self, obj):
        admin = getattr(obj, 'schooladmin', None)
        return admin.id if admin else None


class StudentClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = "__all__"


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class AttendanceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"
