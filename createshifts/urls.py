from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CreateShiftView.as_view(), name='create_shift'),
]
