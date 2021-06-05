from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('guest_login/', views.guest_login, name = 'guest_login')
]
