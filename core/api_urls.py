from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import StaffViewSet, SchoolViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'staff', StaffViewSet)
router.register(r'school', SchoolViewSet)
router.register(r'department', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
