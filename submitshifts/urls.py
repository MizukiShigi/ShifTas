from django.urls import path, include
from submitshifts import views

urlpatterns = [
    path('', views.SubmitShifsView.as_view(), name='submit_shifts'),
]
