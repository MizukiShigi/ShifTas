from datetime import date, datetime, timedelta, timezone
import calendar
import jpholiday

def getCalendarDays(year, month):
    # 曜日を配列に格納
    day_of_week = ['月', '火', '水', '木', '金', '土', '日']

    # 指定年月の1日の曜日と月の日数
    w1, t1 = calendar.monthrange(year,month)
    
    # 日付と曜日を辞書に格納
    days ={}
    for i in range(1, t1+1):
        Date = date(year, month, i)
        
        # 休日かどうか判定
        if w1 >= 5 or jpholiday.is_holiday(Date):
            holiday_flg = True
        else:
            holiday_flg = False
        
        days[i] = {'week': w1, 'day_of_week':day_of_week[w1], 'holiday_flg':holiday_flg}
        
        # 曜日を次の日にずらす
        if w1 < 6:
            w1 += 1
        else:
            w1 = 0
    
    return days