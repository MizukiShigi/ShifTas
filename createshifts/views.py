import staff
from django.shortcuts import render, redirect
from datetime import datetime, time
from django.views.generic import TemplateView
from submitshifts.models import SubmitShift
from .models import ModifyShift, CounterShift, FlyerShift, KitchenShift, CompleteShift 
from django.contrib.auth.models import User
from staff.models import Staff
from common import common, auto_create
from django.contrib.auth import get_user_model
import random

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



