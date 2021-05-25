from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from staff.models import Staff
from submitshifts.models import SubmitShift
from datetime import datetime,time
from common import common
import re

# Create your views here.
class Login(LoginView):
    template_name = 'snipets/auth.html'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class SubmitShifsView(TemplateView):
    template_name = 'shifts/shift_submit.html'
    def get(self, request):
        context = {}
        dt_now = datetime.now()
        year = dt_now.year
        # 月の指定があればその月の表を出力
        if 'month' in request.GET:
            month_str = request.GET.get('month')
            month = int(month_str)
        else:
            month = dt_now.month
        days = common.getCalendarDays(year, month)
        
        staffs = Staff.objects.all()
        request_shift = SubmitShift.objects.filter(year=year, month=month, staff_id=request.user)
        shifts = SubmitShift.objects.filter(year=year, month=month)
        context = {
            'year'          :year, 
            'month'         :month, 
            'this_month'    :dt_now.month, 
            'days'          :days,
            'staffs'        :staffs,
            'request_shift' :request_shift,
            'shifts'        :shifts,
            'range'         :range(1, len(days)+1),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        submit_year = request.POST.get('year')
        submit_month = request.POST.get('month')
        
        # 提出されたシフトで変更や新規登録があったものを更新、追加
        for req in request.POST:
            if 'request' in req:
                submit_day = req.strip('_request')
                request_shift = request.POST.get(req)
                # 更新処理
                try:
                    obj = SubmitShift.objects.get(staff_id=user, year=submit_year, month=submit_month, day=submit_day)
                    if request_shift == 'x':
                        obj.absence_flg = True
                    elif request_shift != '':
                        request_fromtime = int(request_shift[:request_shift.find('-')])
                        request_totime = int(request_shift[request_shift.find('-')+1:])
                        obj.fromtime = request_fromtime
                        obj.totime = request_totime
                        obj.absence_flg = False
                    obj.save()
                # 追加処理
                except SubmitShift.DoesNotExist:
                    new_values = {'staff_id':user, 'year':submit_year, 'month':submit_month, 'day':submit_day}
                    if request_shift == 'x':
                        new_values['absence_flg'] = True
                    elif request_shift != '':
                        request_fromtime = int(request_shift[:request_shift.find('-')])
                        request_totime = int(request_shift[request_shift.find('-')+1:])
                        new_values['fromtime'] = request_fromtime
                        new_values['totime'] = request_totime
                        new_values['absence_flg'] = False
                    obj = SubmitShift(**new_values)
                    obj.save()
        return redirect('submit_shifts')