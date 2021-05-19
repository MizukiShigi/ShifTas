from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from staff.models import Staff
from submitshifts.models import SubmitShift
from datetime import datetime,time
from common import common
import re

# Create your views here.
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
        shifts = SubmitShift.objects.filter(year=year, month=month)
        print(shifts)
        context['year'] = year
        context['month'] = month
        context['this_month'] = dt_now.month
        context['days'] = days
        context['staffs'] = staffs
        context['shifts'] = shifts
        context['range'] = range(1, len(days)+1)
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
                        request_fromtime = time(int(request_shift[:request_shift.find('-')]))
                        request_totime = time(int(request_shift[request_shift.find('-')+1:]))
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
                        request_fromtime = time(int(request_shift[:request_shift.find('-')]))
                        request_totime = time(int(request_shift[request_shift.find('-')+1:]))
                        new_values['fromtime'] = request_fromtime
                        new_values['totime'] = request_totime
                        new_values['absence_flg'] = False
                    obj = SubmitShift(**new_values)
                    obj.save()
        return redirect('submit_shifts')