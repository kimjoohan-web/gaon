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
    "case when lr.status = 'Pending' then '대기' " \
    "     when lr.status = 'Approved' then '승인' " \
    "    when lr.status = 'Rejected' then '반려' " \
    "     else lr.status end as status " \
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
    "lr.created_at, " \
    "case when lr.status = 'Pending' then '대기' " \
    "     when lr.status = 'Approved' then '승인' " \
    "    when lr.status = 'Rejected' then '반려' " \
    "     else lr.status end as status, " \
    "ifnull(la.approval_status,'Pending') approval_status," \
	"ifnull(lb.approval_status,'Pending') t_approval_status " \
    "from vaca_leaverequest lr join auth_user u on lr.user_id_id = u.id " \
    "join vaca_leavetype lt on lr.leave_type_id = lt.leave_type_id " \
    "left join vaca_leaveapproval la on la.leave_request_id=lr.request_id and la.approver_order =1 " \
    "left join vaca_leaveapproval lb on lb.leave_request_id=lr.request_id and lb.approver_order =2 " \
    "where lr.request_id = %s"
    
    # return HttpResponse(sql % request_id)
    leave_request = LeaveRequest.objects.raw(sql, [request_id])[0]

    sql_jik="select id,j_gread from board_jik_gread where j_id_id = %s"
    result=Jik_gread.objects.raw(sql_jik, [request.user.id])[0]
    
    user_jik_gread = result.j_gread if result else 0




    sql_approval = "select approval_id " \
                            ",approver_order " \
                            ",approval_status" \
                            ",approver_order" \
                            ",approver_id_id" \
                            ",leave_request_id" \
                            ",comments" \
                    " from vaca_leaveapproval" \
                    " where leave_request_id =%s and approver_id_id = %s" \
                    " order by approved_at desc limit 1"                    

    leave_approvals = LeaveApproval.objects.raw(sql_approval, [request_id, request.user.id])    
    if leave_approvals:
        leave_approvals = leave_approvals[0]
    else:
        leave_approvals = ''

    
    

    return render(request, 'vaca/leave_detail.html', {'leave_request': leave_request, 'user_jik_gread': user_jik_gread, 'leave_approvals': leave_approvals})  


def vaca_submit(request):
    if request.method == 'POST':
        request_id = request.POST['request_id']
        jik_gread = int(request.POST['jik_gread'])
        leave_status = request.POST['leave_status']
        comments = request.POST['comments']

        if jik_gread == 3 :
            approver_order = 2
        elif jik_gread == 2 :
            approver_order = 1
        else:
            approver_order = 0

        # 먼저 결재 상태 업데이트 및 approver_order 결정
            
        

        if jik_gread == 3: # 대표 결제일때만 결재 상태 업데이트           
            sql_up="update vaca_leaverequest set status = %s where request_id = %s"
            params = (leave_status, request_id)
            cursor = connection.cursor()
            cursor.execute(sql_up, params)
            cursor.close()
            approver_order = 2
        elif jik_gread == 2: # 부장 결제일때만 결재 상태 업데이트
            approver_order = 1
        else:
            approver_order = 0


        sql_ex="select approval_id, approver_order from vaca_leaveapproval where leave_request_id = %s and approver_order = %s order by approved_at desc limit 1"
        result_ex = LeaveApproval.objects.raw(sql_ex, [request_id, approver_order])
        if result_ex:
            sql_up="update vaca_leaveapproval set comments = %s, approved_at = datetime('now', 'localtime'), approval_status = %s where approval_id = %s"
            params_up = (comments, leave_status, result_ex[0].approval_id)
            cursor_up = connection.cursor()
            cursor_up.execute(sql_up, params_up)
            cursor_up.close()
        else:
            sql_in="insert into vaca_leaveapproval (leave_request_id, approver_id_id, comments, approved_at,approval_status,approver_order) values (%s, %s, %s, datetime('now', 'localtime'), %s, %s)"
            params_in = (request_id, request.user.id, comments, leave_status, approver_order)
            cursor_in = connection.cursor()
            cursor_in.execute(sql_in, params_in)
            cursor_in.close()


        return HttpResponse("결재가 완료되었습니다.")
    else:
        return HttpResponse("잘못된 요청입니다.")