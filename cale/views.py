from django.shortcuts import render
from datetime import datetime
import calendar
# Create your views here.
def cale_list(request):
    introduce_data = {}
    # introduce_data = {'main_view': main_view, 'total_count': total_count} #기존 데이터



    year = datetime.now().year
    month = datetime.now().month    
    today = datetime.today()
    
    introduce_data['today'] = today
    introduce_data['month'] = month
    introduce_data['year'] = year

    #새로 추가된 코드
    cal = calendar.monthcalendar(year, month)
    cal_data = []

    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append((None, None))
            else:
                count = 1 #호출 데이터
                week_data.append((day, count))
        cal_data.append(week_data)

    introduce_data['cal_data'] = cal_data


    return render(request, 'cale/cale_list.html', introduce_data)
    