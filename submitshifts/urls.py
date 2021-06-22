from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.SubmitShifsView.as_view(), name='submit_shifts'),
    path('export/<int:year>/<int:month>', views.export, name='submited_export'),
]
