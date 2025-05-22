from rest_framework.views import APIView
from .models import Staff, Department, School, StudentClass, Student, Attendance
from .serializers import StaffSerializers, DepartmentSerializers, SchoolSerializers, StudentClassSerializers, \
    StudentSerializers, AttendanceSerializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class StaffBySchoolDepartment(APIView):

    def get(self, request, school_id, department_id, staff_id=None):
        if staff_id is not None:
            staff = Staff.objects.filter(
                id=staff_id,
                school_id=school_id,
                department_id=department_id
            ).first()

            if not staff:
                return Response({"detail": "Staff not found"}, status=404)

            serializer = StaffSerializers(staff)
            return Response(serializer.data)

        staff_qs = Staff.objects.filter(
            school_id=school_id,
            department_id=department_id
        )
        serializer = StaffSerializers(staff_qs, many=True)
        return Response(serializer.data)


class DepartmentBySchool(APIView):

    def get(self, request, school_id):
        department_qs = Department.objects.filter(
            school_id=school_id
        )
        serializer = DepartmentSerializers(department_qs, many=True)
        return Response(serializer.data)


class StudentClassView(APIView):

    def get(self, request, school_id):
        class_qs = StudentClass.objects.filter(school_id=school_id)
        serializer = StudentClassSerializers(class_qs, many=True)
        return Response(serializer.data)


class SchoolView(APIView):

    def get(self, request, school_id=None):
        if school_id is not None:
            school = get_object_or_404(School, id=school_id)
            serializer = SchoolSerializers(school)
            return Response(serializer.data)

        else:
            schools = School.objects.all()
            serializer = SchoolSerializers(schools, many=True)
            return Response(serializer.data)


class StudentView(APIView):

    def get(self, request, school_id, class_id):
        student_qs = Student.objects.filter(
            school_id=school_id,
            student_class_id=class_id
        )
        serializer = StudentSerializers(student_qs, many=True)
        return Response(serializer.data)


class AttendanceView(APIView):

    def get(self, request, school_id, department_id, staff_id):
        staff_attendance = Attendance.objects.filter(
            school_id=school_id,
            department_id=department_id,
            staff_id=staff_id
        )
        serializer = AttendanceSerializers(staff_attendance, many=True)
        return Response(serializer.data)
