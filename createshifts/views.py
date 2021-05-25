from django.shortcuts import render, redirect
from datetime import datetime, time
from django.views.generic import TemplateView
from submitshifts.models import SubmitShift
from .models import ModifyShift, CounterShift, FlyerShift, KitchenShift, CompleteShift 
from django.contrib.auth.models import User
from staff.models import Staff
from common import common
from django.contrib.auth import get_user_model
import random

# Create your views here.

# グローバル変数
dt_now = datetime.now()
year = dt_now.year
month = dt_now.month
days = common.getCalendarDays(year, month)

class CreateShiftView(TemplateView):
    template_name = 'shifts/shift_complete.html'
    def get(self, request):
        shift = CompleteShift.objects.filter(year=year, month=month)
        context = {'year':year, 'month':month, 'shift':shift, 'days':days}
        return render(request, self.template_name, context)
    
    def post(self, request):
        auto_create()
        return redirect('create_shift')

# シフト自動作成
def auto_create():
    global days
    # 1日ずつ作成する
    for day in days:
        day_shift_data = create_position_shift(day)

def create_position_shift(day):
    global year
    global month
    get_flyer_shifts = SubmitShift.objects.filter(year=year, month=month, day=day, absence_flg=False)
    get_open_shifts = get_flyer_shifts.filter(staff_id__staff__responsible_flg=True, staff_id__staff__opener_flg=True).values('id','staff_id_id','fromtime','totime')
    get_close_shifts = get_flyer_shifts.filter(staff_id__staff__responsible_flg=True).values('id','staff_id_id','fromtime','totime')
    get_counter_shifts = SubmitShift.objects.filter(staff_id__staff__counter_flg=True).values('id','staff_id_id','fromtime','totime')
    get_kitchen_shifts = SubmitShift.objects.filter(staff_id__staff__kitchen_flg=True).values('id','staff_id_id','fromtime','totime')
    
    flyer_shifts = create_flyer_shift(get_open_shifts, get_close_shifts)
    flyer_id = save_shift('flyer', flyer_shifts) 
    print(flyer_id)
    counter_shifts = create_counter_shift(get_counter_shifts)
    kitchen_shifts = create_kitchen_shift(get_kitchen_shifts)

def create_flyer_shift(open_shifts, close_shifts):
    
    #-------------変数初期化------------#
    selected_flyer = {
        'am_1':{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None}, 
        'am_2':{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None}, 
        'pm_1':{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None}, 
        'pm_2':{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None}
    }
    open_candidate1 = []
    open_candidate2 = []
    close_candidate1 = []
    close_candidate2 = []
    str_am_1 = '{}'
    str_am_2 = '{}'
    baton_am_pm = 17
    #------------------------------------#

    # オープンの候補者をリストに格納
    for open in open_shifts:
        # オープンから5時間以上入れる候補者
        if open['fromtime'] == 9 and (open['totime']-open['fromtime']) >= 5:
            open_candidate1.append(open)
        elif open['fromtime'] <= 12 and (open['totime']-open['fromtime']) >= 5:
            open_candidate2.append(open)
    # オープン作業者を決定
    if len(open_candidate1) > 0:
        selected_flyer['am_1'] = random.choice(open_candidate1)
        am_1 = selected_flyer['am_1'].copy()
        # 引継ぎ先の時間を指定
        if selected_flyer['am_1']['totime'] >= 17:
            selected_flyer['am_1']['totime'] = 17
        else:
            # 午後の開始時間を午前のスタッフの終了時間に変更
            baton_am_pm = selected_flyer['am_1']['totime']
    elif len(open_candidate2) > 0:
        # 最も早く入れるスタッフの時間を変数に格納
        baton_am = min(candidate['fromtime'] for candidate in open_candidate2)
        # シフトの空きを作る
        selected_flyer['am_1'] = {'id':None, 'staff_id_id': None, 'fromtime': 9, 'totime': baton_am}
        selected_flyer['am_2'] = [candidate for candidate in open_candidate2 if candidate['fromtime'] == baton_am][0]
        am_2 = selected_flyer['am_2'].copy()
        if selected_flyer['am_2']['totime'] >= 17:
            selected_flyer['am_2']['totime'] = 17
        else:
            # 午後の開始時間を午前のスタッフの終了時間に変更
            baton_am_pm = selected_flyer['am_2']['totime']
    else:
        selected_flyer['am_1'] = {'id':None, 'staff_id_id': None, 'fromtime': 9, 'totime': 17}
    
    # クローズ候補者 (引継ぎの時間以下からクローズまで入れるスタッフを格納)
    for close in close_shifts:
        if close['fromtime'] <= baton_am_pm and close['totime'] == 21:
            close_candidate1.append(close)
        elif close['fromtime'] <= 18 and close['totime'] == 21:
            close_candidate2.append(close)
    # オープンに入った人はクローズの候補者から削除。ただし、1人しか候補者がいない場合は残す。
    if len(close_candidate1) > 1:
        if am_1 in close_candidate1:
            close_candidate1.remove(am_1)
        elif am_2 in close_candidate1:
            close_candidate1.remove(am_2)
    # クローズ作業者を決定
    if len(close_candidate1) > 0:
        selected_flyer['pm_1'] = random.choice(close_candidate1)
        # クローズ作業者の開始時間を引継ぎ時間に変更
        selected_flyer['pm_1']['fromtime'] = baton_am_pm
    elif len(close_candidate2) > 0:
        selected_flyer['pm_2'] = random.choice(close_candidate2)
        selected_flyer['pm_1']['fromtime'] = baton_am_pm
        selected_flyer['pm_1']['totime']   = selected_flyer['pm_2']['fromtime']
    else:
        selected_flyer['pm_1']['fromtime'] = baton_am_pm
        selected_flyer['pm_1']['totime']   = 21
    print(selected_flyer)
    return selected_flyer

def create_counter_shift(counter_shifts):
    return None

def create_kitchen_shift(kitchen_shifts):
    return None
    
def save_shift(position, shifts):
    if position == 'flyer':
        flyer_params = {}
        if shifts['am_1']['fromtime'] is not None:
            submit_id = SubmitShift.objects.get(pk=shifts['am_1']['id']) if shifts['am_1']['id'] is not None else None
            flyer_params['am_1'] = am_1 = ModifyShift.objects.create(submit_id=submit_id, position='flyer', modify_fromtime=shifts['am_1']['fromtime'], modify_totime=shifts['am_1']['totime'])
        
        if shifts['am_2']['fromtime'] is not None:
            submit_id = SubmitShift.objects.get(pk=shifts['am_2']['id']) if shifts['am_2']['id'] is not None else None
            flyer_params['am_2'] = am_2 = ModifyShift.objects.create(submit_id=submit_id, position='flyer', modify_fromtime=shifts['am_2']['fromtime'], modify_totime=shifts['am_2']['totime'])
        
        if shifts['pm_1']['fromtime'] is not None:
            submit_id = SubmitShift.objects.get(pk=shifts['pm_1']['id']) if shifts['pm_1']['id'] is not None else None
            flyer_params['pm_1'] = pm_1 = ModifyShift.objects.create(submit_id=submit_id, position='flyer', modify_fromtime=shifts['pm_1']['fromtime'], modify_totime=shifts['pm_1']['totime'])
            
        if shifts['pm_2']['fromtime'] is not None:
            submit_id = SubmitShift.objects.get(pk=shifts['pm_2']['id']) if shifts['pm_2']['id'] is not None else None
            flyer_params['pm_2'] = pm_2 = ModifyShift.objects.create(submit_id=submit_id, position='flyer', modify_fromtime=shifts['pm_2']['fromtime'], modify_totime=shifts['pm_2']['totime'])
        
        if len(flyer_params):
            flyer = FlyerShift(**flyer_params)
            flyer.save()
            flyer_id = flyer.pk

    return flyer_id


