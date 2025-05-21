from django.urls import path
from .api_views import StaffBySchoolDepartment, DepartmentBySchool, SchoolView

urlpatterns = [
    path('school/<int:school_id>/department/<int:department_id>/staff/', StaffBySchoolDepartment.as_view(),
         name='staff-by-department'),
    path('school/<int:school_id>/department/', DepartmentBySchool.as_view(), name='department-by-school'),
    path('school/', SchoolView.as_view(), name='schools-list'),
    path('school/<int:school_id>/', SchoolView.as_view(), name='schools-by-id')

]
