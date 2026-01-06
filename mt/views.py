from urllib import request, response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import company_info, subject_db
from django.shortcuts import render
import requests
# Create your views here.
@login_required(login_url='common:login')
def index(request):
    
    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')    
    subject_gubun = request.GET.get('subject_gubun','')    
    
    if subject_gubun is None or subject_gubun =='':
        subject_gubun ='0'
    # category_list = Catogory.objects.all()
    # su_list = subject_db.objects.all().order_by('-s_idx')

    SQL ="select A.*,B.c_name,strftime('%Y-%m-%d', A.start_date) startdate " 
    SQL += " ,(A.sum_total-A.su_total) misu_total ,A.su_total ,A.etc_total "
    SQL += " ,strftime('%Y-%m-%d', A.end_date) enddate "
    SQL += " ,cast((julianday(A.end_date) - julianday('now')) as INTEGER)  date_cha "
    SQL += " from mt_subject_db A LEFT JOIN mt_company_info B on A.c_idx_id=B.c_idx  "
    if kw:
        SQL += " where B.c_name like '%%"+kw+"%%' "
        SQL += " or A.s_title like '%%"+kw+"%%' "

    if subject_gubun :
        if 'where' in SQL:
            SQL += " and A.s_gubun = "+subject_gubun+" "
        else:
            SQL += " where A.s_gubun = "+subject_gubun+" "    
    
    SQL += " order by A.s_idx desc "
    su_list = subject_db.objects.raw(SQL)

    
    paginator = Paginator(su_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context ={'su_list':page_obj,'page':page,'kw':kw ,'subject_gubun':subject_gubun}
    return render(request, 'mt/index.html',context)



def status(request):
    url = 'http://apis.data.go.kr/B490007/emonService/stAgentYearlyService/stAgentYearlyInfo'
    params ={'serviceKey' : '6e9bf5d2f8bdc3efb21e12e806094b3abb6f8b45c6104bf76282daa462df78ce', 'pageNo' : '1', 'numOfRow' : '10' }

    response = requests.get(url, params=params)
    context ={'status_to':response.content}
    return render(request, 'mt/status.html',context)
    # print(response.content)