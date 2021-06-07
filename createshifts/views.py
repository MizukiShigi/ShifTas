from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import  CompleteShift 
from django.contrib.auth.models import User
from staff.models import Staff
from common import auto_create

# Create your views here.

class CreateShiftView(TemplateView):
    template_name = 'shifts/shift_complete.html'
    def get(self, request):
        shift = CompleteShift.objects.filter(year=auto_create.year, month=auto_create.month)
        status = Staff.objects.get(staff_id=request.user)
        context = {'year':auto_create.year, 'month':auto_create.month, 'shift':shift, 'days':auto_create.days, 'status':status}
        return render(request, self.template_name, context)
    
    def post(self, request):
        auto_create.auto_create()
        return redirect('create_shift')



