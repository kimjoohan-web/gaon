from urllib import response
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render 
from django.core.paginator import Paginator
from vaca.models import LeaveType, LeaveBalance, LeaveRequest, LeaveApproval
from board.models import Jik_gread
# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    
    sql="select lr.request_id, " \
    "lr.user_id_id, " \
    "u.username, " \
    "lt.type_name, " \
    "lr.start_date, " \
    "lr.end_date, " \
    "lr.reason, " \
    "lr.status  " \
    "from vaca_leaverequest lr join auth_user u on lr.user_id_id = u.id " \
    "join vaca_leavetype lt on lr.leave_type_id = lt.leave_type_id " \
    "order by lr.created_at desc"

    # return HttpResponse(sql)
    leave_requests = LeaveRequest.objects.raw(sql)

    paginator = Paginator(leave_requests, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context ={'leave_requests':page_obj,'page':page}
    
    
    return render(request, 'vaca/leave_index.html', context)   


def leave_request(request):
    sql_type = "select leave_type_id, type_name from vaca_leavetype order by leave_type_id asc"
    leave_types = LeaveType.objects.raw(sql_type)   

    if request.method == 'POST':
        # 폼에서 제출된 데이터를 처리하는 로직을 여기에 작성
        # 예: 휴가 신청 데이터를 저장하거나 검증하는 코드
        leave_type = request.POST['leave_type']  # 예시로 leave_type을 가져오는 코드
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']
        status = 'Pending'  # 기본적으로 신청 상태는 'Pending'으로 설정

        sql_in="insert into vaca_leaverequest (user_id_id, leave_type_id, start_date, end_date, reason, status, created_at) values (%s, %s, %s, %s, %s, %s, datetime('now', 'localtime'))"
        params = (request.user.id, leave_type, start_date, end_date, reason, status)
        cursor = connection.cursor()
        cursor.execute(sql_in, params)
        cursor.close()


        # return HttpResponse(sql_in % params)  # SQL 쿼리와 파라미터를 출력하여 확인
    
        return redirect('vaca:index')
    else:   
        return render(request, 'vaca/leave_request.html', {'leave_types': leave_types})
    

def leave_detail(request, request_id):
    sql="select lr.request_id, " \
    "lr.user_id_id, " \
    "u.username, " \
    "lt.type_name, " \
    "lr.start_date, " \
    "lr.end_date, " \
    "lr.reason, " \
    "lr.status  " \
    "from vaca_leaverequest lr join auth_user u on lr.user_id_id = u.id " \
    "join vaca_leavetype lt on lr.leave_type_id = lt.leave_type_id " \
    "where lr.request_id = %s"

    leave_request = LeaveRequest.objects.raw(sql, [request_id])[0]

    sql_jik="select id,j_gread from board_jik_gread where j_id_id = %s"
    result=Jik_gread.objects.raw(sql_jik, [request.user.id])[0]
    
    user_jik_gread = result.j_gread if result else 0


    return render(request, 'vaca/leave_detail.html', {'leave_request': leave_request, 'user_jik_gread': user_jik_gread})  
