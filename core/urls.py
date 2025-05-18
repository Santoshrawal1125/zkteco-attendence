from django.urls import path
from . import views


urlpatterns = [
    path('cdata', views.iclock_cdata, name='iclock_cdata'),
    path('getrequest', views.get_request),
]
