from datetime import datetime, time
from submitshifts.models import SubmitShift
from createshifts.models import ModifyShift, CounterShift, FlyerShift, KitchenShift, CompleteShift 
from . import common 
from django.db import connection
import random

# グローバル変数
dt_now = datetime.now()
year = dt_now.year
month = dt_now.month + 1
days = common.getCalendarDays(year, month)

# シフト自動作成
def auto_create():
    global year
    global month
    global days
    # 既に今月のシフトが作成済みの場合は既存シフトを削除
    if CompleteShift.objects.filter(year=year, month=month).exists():
        CompleteShift.objects.all().delete()
    # 1日ずつ作成する
    for day, value in days.items():
        if value['holiday_flg'] == True or day == 28: 
            holiday = True
        else: 
            holiday = False
        day_shift_data = create_position_shift(day, holiday)

def create_position_shift(day, is_holiday):
    global year
    global month
    # フライヤーポジションのスタッフを取得
    get_flyer_shifts = SubmitShift.objects.filter(year=year, month=month, day=day, absence_flg=False)
    get_open_shifts = get_flyer_shifts.filter(staff_id__responsible_flg=True, staff_id__opener_flg=True).values('id','staff_id_id','fromtime','totime')
    get_close_shifts = get_flyer_shifts.filter(staff_id__responsible_flg=True).values('id','staff_id_id','fromtime','totime')
    flyer_shifts = create_flyer_shift(get_open_shifts, get_close_shifts)
    flyer_id = save_shift('flyer', flyer_shifts) 
    
    # カウンターポジションのスタッフを取得
    get_counter_shifts = list(
                            SubmitShift.objects\
                            .filter(year=year, month=month, day=day, absence_flg=False, staff_id__counter_flg=True)\
                            .exclude(pk__in=ModifyShift.objects.filter(submit_id__year=year, submit_id__month=month, submit_id__day=day).values_list('submit_id'))\
                            .values('id','staff_id_id','fromtime','totime')
                            )
    counter_shifts = create_counter_shift(get_counter_shifts, is_holiday)
    counter_id = save_shift('counter', counter_shifts)
    
    # キッチンポジションのスタッフを取得
    get_kitchen_shifts = list(
                            SubmitShift.objects\
                            .filter(year=year, month=month, day=day, absence_flg=False, staff_id__kitchen_flg=True)\
                            .exclude(pk__in=ModifyShift.objects.filter(submit_id__year=year, submit_id__month=month, submit_id__day=day).values('submit_id'))\
                            .values('id','staff_id_id','fromtime','totime')
                            )
    kitchen_shifts = create_kitchen_shift(get_kitchen_shifts, is_holiday)
    kitchen_id = save_shift('kitchen', kitchen_shifts)

    complete_shift = CompleteShift(year=year, month=month, day=day, is_holiday=is_holiday, flyer_shift=flyer_id, counter_shift=counter_id, kitchen_shift=kitchen_id)
    complete_shift.save()

def create_flyer_shift(open_shifts, close_shifts):
    
    #-------------変数初期化------------#
    delimiter_time = ['am_1','am_2','pm_1','pm_2']
    selected_flyer = {
        delimiter_time[i]:{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None} for i in range(4)
    }
    open_candidates1     = []
    open_candidates1_sub = []
    close_candidates1    = []
    close_candidates2    = []
    baton_op_cl = 0
    #------------------------------------#

    # オープンの候補者をリストに格納
    for open in open_shifts:
        select_am_flyer_candidates(open, open_candidates1, open_candidates1_sub)
    # オープン作業者を決定
    am_1= create_am_shift('am_1', 9, 17, selected_flyer, open_candidates1, open_candidates1_sub)
    baton_op_cl = selected_flyer['am_1']['totime']
    
    # クローズ候補者 (引継ぎの時間以下からクローズまで入れるスタッフを格納)
    for close in close_shifts:
        select_pm_flyer_candidates(close, baton_op_cl, close_candidates1, close_candidates2)
    # クローズ作業者を決定
    create_pm_shift('pm_1', 'pm_2', baton_op_cl, selected_flyer, close_candidates1, close_candidates2)
    print(selected_flyer)
    return selected_flyer

def create_counter_shift(counter_shifts, holiday):
    #-------------変数初期化------------#
    delimiter_time = ['am_1','am_2','am_3','am_4','am_5', 'pm_1','pm_2','pm_3','pm_4', 'pm_5', 'pm_6']
    selected_counter = {
        delimiter_time[i]:{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None} for i in range(11)
    }
    
    am1_candidates       = []
    am1_candidates_sub   = []
    am2_candidates       = []
    am2_candidates_sub   = []
    am3_candidates       = []
    am3_candidates_sub   = []
    am4_candidates       = []
    am5_candidates       = []
    pm1_candidates       = []
    pm1_candidates_sub   = []
    pm2_candidates       = []
    pm2_candidates_sub   = []
    pm3_candidates       = []
    pm3_candidates_sub   = []
    
    # pmは最大3人なのでバトンは3つ用意
    baton_am1_pm1 = 0
    baton_am2_pm2 = 0
    baton_am3_pm3 = 0
    #------------------------------------#  
    
    # amの候補者を選定
    for counter in counter_shifts:
        select_am_counter_candidates(counter, am1_candidates, am1_candidates_sub ,am2_candidates, am2_candidates_sub, am3_candidates, am3_candidates_sub, am4_candidates, am5_candidates)

    # am1のスタッフをランダム抽出
    tmp_list = [am2_candidates, am2_candidates_sub, am3_candidates, am3_candidates_sub, am4_candidates, am5_candidates]
    am_1 = create_am_shift('am_1', 9, 17, selected_counter, am1_candidates, am1_candidates_sub, tmp_list)
    baton_am1_pm1 = selected_counter['am_1']['totime']

    # am2のスタッフをランダム抽出
    tmp_list = [am3_candidates, am3_candidates_sub, am4_candidates, am5_candidates]
    am_2 = create_am_shift('am_2', 10, 17, selected_counter, am2_candidates, am2_candidates_sub, tmp_list)
    baton_am2_pm2 = selected_counter['am_2']['totime']
    
    # am3のスタッフをランダム抽出
    tmp_list = [am4_candidates, am5_candidates]
    am_3 = create_am_shift('am_3', 11, 17, selected_counter, am3_candidates, am3_candidates_sub, tmp_list)
    baton_am3_pm3 = selected_counter['am_3']['totime']

    # am4のスタッフをランダム抽出
    if holiday:
        tmp_list = [am5_candidates]
        am_4 = create_am_shift('am_4', 12, 17, selected_counter, am4_candidates, tmp_list=tmp_list)
    else:
        am_4 = None
    # am5のスタッフをランダム抽出
    if holiday:
        am_5 = create_am_shift('am_5', 12, 17, selected_counter, am5_candidates)
    else:
        am_5 = None
    
    # pmの候補者を選定
    for counter in counter_shifts:
        select_pm_counter_candidates(counter, baton_am1_pm1, pm1_candidates, [am_1, am_2, am_3, am_4, am_5])
        select_pm_counter_candidates(counter, baton_am2_pm2, pm2_candidates, [am_1, am_2, am_3, am_4, am_5])
        select_pm_counter_candidates(counter, baton_am3_pm3, pm3_candidates, [am_1, am_2, am_3, am_4, am_5])
    
    # pm1のスタッフをランダム抽出
    tmp_list = [pm2_candidates, pm2_candidates_sub, pm3_candidates, pm3_candidates_sub]
    create_pm_shift('pm_1', 'pm_4', baton_am1_pm1, selected_counter, pm1_candidates, pm1_candidates_sub, tmp_list)

    # pm2のスタッフをランダム抽出
    tmp_list = [pm3_candidates, pm3_candidates_sub]
    create_pm_shift('pm_2', 'pm_5', baton_am2_pm2, selected_counter, pm2_candidates, pm2_candidates_sub, tmp_list)

    # pm3のスタッフをランダム抽出
    create_pm_shift('pm_3', 'pm_6', baton_am3_pm3, selected_counter, pm3_candidates, pm3_candidates_sub)

    print(selected_counter)
    return selected_counter

def create_kitchen_shift(kitchen_shifts, holiday):
    #-------------変数初期化------------#
    delimiter_time = ['am_1','am_2','pm_1','pm_2']
    selected_kitchen = {
        delimiter_time[i]:{'id':None, 'staff_id_id': None, 'fromtime': None, 'totime': None} for i in range(4)
    }
    
    am1_candidates       = []
    am1_candidates_sub   = []
    am2_candidates       = []
    pm1_candidates       = []
    pm2_candidates       = []
    
    # pmは最大3人なのでバトンは3つ用意
    baton_am1_pm1 = 0
    baton_am2_pm2 = 0
    #------------------------------------#  
    
    # amの候補者を選定
    for kitchen in kitchen_shifts:
        select_am_kitchen_candidates(kitchen, am1_candidates, am1_candidates_sub ,am2_candidates)

    # am1のスタッフをランダム抽出
    tmp_list = [am2_candidates]
    am_1 = create_am_shift('am_1', 9, 17, selected_kitchen, am1_candidates, am1_candidates_sub, tmp_list)
    baton_am1_pm1 = selected_kitchen['am_1']['totime']

    # am2のスタッフをランダム抽出
    if holiday:
        am_2 = create_am_shift('am_2', 12, 17, selected_kitchen, am2_candidates)
    else:
        am_2 = None
    baton_am2_pm2 = 17
    
    # pmの候補者を選定
    for kitchen in kitchen_shifts:
        select_pm_kitchen_candidates(kitchen, baton_am1_pm1, pm1_candidates, [am_1, am_2])
        select_pm_kitchen_candidates(kitchen, baton_am2_pm2, pm2_candidates, [am_1, am_2])
    
    # pm1のスタッフをランダム抽出
    tmp_list = [pm2_candidates]
    create_pm_shift('pm_1', 'pm_3', baton_am1_pm1, selected_kitchen, pm1_candidates, tmp_list=tmp_list)

    # pm2のスタッフをランダム抽出
    create_pm_shift('pm_2', 'pm_4', baton_am2_pm2, selected_kitchen, pm2_candidates)

    print(selected_kitchen)
    return selected_kitchen

def select_am_flyer_candidates(flyer, am1, am1_sub):
    if   flyer['fromtime'] == 9 and flyer['totime'] >= 17 : am1.append(flyer)
    elif flyer['fromtime'] == 9 and flyer['totime'] >= 14 : am1_sub.append(flyer)

def select_pm_flyer_candidates(flyer, baton, pm1, pm2):
    if flyer['fromtime'] <= baton and flyer['totime'] == 21:
        pm1.append(flyer)
    elif flyer['fromtime'] <= 17 and flyer['totime'] == 21:
        pm2.append(flyer)

def select_am_counter_candidates(counter, am1, am1_sub, am2, am2_sub, am3, am3_sub, am4, am5):
    if counter['fromtime'] == 9:
        if counter['totime'] >= 17 : am1.append(counter)
        elif counter['totime'] >= 14 : am1_sub.append(counter)
    
    if counter['fromtime'] <= 10:
        if counter['totime'] >= 17 : am2.append(counter)
        elif counter['totime'] >= 15 : am2_sub.append(counter)
    
    if counter['fromtime'] <= 11:
        if counter['totime'] >= 17 : am3.append(counter)
        elif counter['totime'] >= 16 : am3_sub.append(counter)
    
    if counter['fromtime'] <= 12 and counter['totime'] >= 17:
        am4.append(counter)
        am5.append(counter)

def select_pm_counter_candidates(counter, baton, pm, am_list):
    if counter['fromtime'] <= baton and counter['totime'] == 21:
        if baton < 17:
            if counter not in am_list: 
                pm.append(counter)
        else:
            pm.append(counter)

def select_am_kitchen_candidates(kitchen, am1, am1_sub, am2):
    if   kitchen['fromtime'] == 9 and kitchen['totime'] >= 17 : am1.append(kitchen)
    elif kitchen['fromtime'] == 9 and kitchen['totime'] >= 14 : am1_sub.append(kitchen)
    if kitchen['fromtime'] <= 12 and kitchen['totime'] >= 17 : am2.append(kitchen)

def select_pm_kitchen_candidates(kitchen, baton, pm, am_list):
    if kitchen['fromtime'] <= baton and kitchen['totime'] == 21:
        if baton < 17:
            if kitchen not in am_list: 
                pm.append(kitchen)
        else:
            pm.append(kitchen)

def create_am_shift(delimiter, fromtime, totime, selected_position, candidates, next_candidates={}, tmp_list=[]):
    # amのスタッフをランダム抽出
    if len(candidates) > 0:
        am_staff = choice_am_staff(delimiter, fromtime, selected_position, candidates)
    elif len(next_candidates) > 0:
        am_staff = choice_am_staff(delimiter, fromtime, selected_position, next_candidates)
    else:
        # スタッフが足りないシフトを作成
        am_staff = selected_position[delimiter]
        selected_position[delimiter]['fromtime'] = fromtime
        selected_position[delimiter]['totime'] = totime
    # 選出されたスタッフを他の候補から削除
    if am_staff['id'] is not None:
        candidates_remove(tmp_list, am_staff)
    return am_staff

def create_pm_shift(delimiter, for_blank_delimiter, baton, selected_position, candidates, next_candidates={}, tmp_list=[]):
    if len(candidates) > 0:
        pm_staff = choice_pm_staff(delimiter, baton, selected_position, candidates)
    elif len(next_candidates) > 0:
        if baton < 17:
            # スタッフが足りないシフトを作成
            selected_position[for_blank_delimiter]['fromtime'] = baton
            selected_position[for_blank_delimiter]['totime'] = 17
        pm_staff = choice_pm_staff(delimiter, baton, selected_position, next_candidates)
    else:
        # スタッフが足りないシフトを作成
        pm_staff = selected_position[delimiter]
        selected_position[delimiter]['fromtime'] = baton
        selected_position[delimiter]['totime'] = 21
    # 選出されたスタッフを他の候補から削除
    if pm_staff['id'] is not None:
        candidates_remove(tmp_list, pm_staff)
    
def choice_am_staff(am, fromtime, selected_position, candidate_list):
    selected_position[am] = random.choice(candidate_list).copy()
    am_staff = selected_position[am].copy()
    # 開始時間を指定の時間に変更
    selected_position[am]['fromtime'] = fromtime
    # 引継ぎ先の時間を指定
    if selected_position[am]['totime'] >= 17:
        selected_position[am]['totime'] = 17
    return am_staff

def choice_pm_staff(pm, fromtime, selected_position, candidate_list):
    selected_position[pm] = random.choice(candidate_list).copy()
    pm_staff = selected_position[pm].copy()
    # 開始時間を指定の時間に変更
    selected_position[pm]['fromtime'] = fromtime
    return pm_staff

def candidates_remove(candidates_list, delete_target):
    for candidates in candidates_list:
        if delete_target in candidates: candidates.remove(delete_target) 

    
def save_shift(position, shifts):
    params = {}
    if position in ['flyer', 'kitchen']:
        keys = ['am_1', 'am_2', 'pm_1', 'pm_2']
    elif position == 'counter':
        keys = ['am_1', 'am_2', 'am_3', 'am_4', 'am_5', 'pm_1','pm_2', 'pm_3', 'pm_4','pm_5', 'pm_6']
    
    for i in range(len(keys)):
        if shifts[ keys[i] ]['fromtime'] is not None:
            submit_id = SubmitShift.objects.get(pk=shifts[ keys[i] ]['id']) if shifts[ keys[i] ]['id'] is not None else None
            params[ keys[i] ] = ModifyShift.objects.create(submit_id=submit_id, position=position, modify_fromtime=shifts[ keys[i] ]['fromtime'], modify_totime=shifts[ keys[i] ]['totime'])
    if len(params) > 0 :
        if position == 'flyer':
            flyer = FlyerShift(**params)
            flyer.save()
            save_id = flyer
        elif position == 'counter':
            counter = CounterShift(**params)
            counter.save()
            save_id = counter
        elif position == 'kitchen':
            kitchen = KitchenShift(**params)
            kitchen.save()
            save_id = kitchen

    
    return save_id
