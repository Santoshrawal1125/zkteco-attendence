from rest_framework.views import APIView
from .models import Staff, Department, School
from .serializers import StaffSerializers, DepartmentSerializers, SchoolSerializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class StaffBySchoolDepartment(APIView):

    def get(self, request, school_id, department_id):
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
