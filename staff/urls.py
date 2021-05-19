from django.urls import path, include
from staff import views

urlpatterns = [
    path('', views.StaffListView.as_view(), name='staff_list'),
    path('<int:pk>', views.StaffDetailView.as_view(), name='staff_detail'),
]
