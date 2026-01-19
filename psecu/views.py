from email.mime import message
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator


from .models import pc_secu_title_db, pc_secu_ck_db, pc_secu_cf_db, pc_work_board_db
from board.models import Jik_gread
from django.contrib.auth.decorators import login_required
from datetime import datetime as time, timezone
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect
from django import forms # 추가
from .form import Pc_secu_ck_Form
from django.core import serializers
import json


# Create your views here.
def login_gik_gread(user_id):
    SQL = "select j_gread from board_jik_gread where j_id_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(SQL, [user_id])
        result = cursor.fetchone()
        return result[0] if result else None


def index(request):    
    # p_m_idx = models.AutoField(primary_key=True)
    # p_m_b=models.IntegerField()
    # p_m_m=models.IntegerField()
    # p_m_s=models.IntegerField()
    # p_m_title=models.CharField(max_length=400)
    # p_m_indate=models.DateTimeField()
    # p_m_YN=models.CharField(max_length=1)
    # p_m_asc=models.IntegerField()
    

    #먼저 로그인 했을때 직급확인 

    j_gread = login_gik_gread (request.user.id)
    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')


    SQL = " select A.p_wb_idx " 
    SQL +=",A.p_wb_b,A.p_wb_id_id,A.p_wb_indate,A.p_wb_wdate " 
    SQL +=",B.username "    
    SQL += " from psecu_pc_work_board_db A left JOIN auth_user B on A.p_wb_id_id = B.id "
    if j_gread == 1:  # 일반사원
        SQL += " where A.p_wb_id_id=" + str(request.user.id)              
    SQL += " order by A.p_wb_wdate desc "

    ps_list = pc_work_board_db.objects.raw(SQL)
    paginator = Paginator(ps_list, 30)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
 
    toDay = time.now().strftime('%Y-%m-%d')    
    context ={'ps_list':page_obj,'page':page,'kw':kw }
    return render(request, 'psecu/psecu_list.html',context)

def psecu_submit(request):
    p_m_val = ""
    p_m_b = 1
    if request.method == 'POST':        
        username = request.user.get_username()
        useridx = request.user.id
        toDay = time.now().strftime('%Y-%m-%d')
        #  request.POST['b_link_one']
        p_m_c_val_list = request.POST.keys()          
        p_m_c_wdate=request.POST.get('p_m_c_wdate')

        if p_m_c_wdate == None or p_m_c_wdate == '':
            messages.error(request, '작업 일자가 없습니다')            
            return redirect('psecu:psecu_submit')

        p_m_b=request.POST.get('p_m_b')
        if not p_m_b:
            p_m_b = 1



        SQL1 = "insert into psecu_pc_work_board_db (p_wb_b, p_wb_id_id, p_wb_indate, p_wb_wdate,p_wb_check,p_wb_review_check) "
        SQL1 += " values (%s,%s,%s,%s,%s,%s) "
        # return HttpResponse(useridx )
        with connection.cursor() as cursor:
            cursor.execute(SQL1, [p_m_b, useridx, toDay, p_m_c_wdate,'N','N'])  
        # 마지막으로 입력된 p_wb_idx 값 가져오기
        SQL2 = "SELECT last_insert_rowid() as last_id" 
        with connection.cursor() as cursor:
            cursor.execute(SQL2)
            result = cursor.fetchone()
            last_p_wb_idx = result[0] if result else None


        for key in p_m_c_val_list:            
           
           if key.startswith('psecu_'):                 
                # p_m_val =  key + "_" + request.POST.get(key) + "," + p_m_val
                p_m_idx_id = key.split('_')[1]   
                p_m_val =  request.POST.get(key)
                SQL = "insert into psecu_pc_secu_ck_db (p_m_idx_id, p_m_c_val, p_m_c_id_id, p_m_c_indate,p_m_c_wdate,p_m_b,p_wb_idx) "
                SQL += " values (%s,%s,%s,%s,%s,%s,%s) "
                # return HttpResponse(useridx )
                with connection.cursor() as cursor:
                    cursor.execute(SQL, [p_m_idx_id, p_m_val, useridx, toDay, p_m_c_wdate, p_m_b,last_p_wb_idx]) 
         
        return redirect('psecu:index')
    else:
        
        # p_m_b 최대값 구하기
        SQL = "select p_m_b,p_m_idx from psecu_pc_secu_title_db order by p_m_b DESC LIMIT 1"
        ps_b = pc_secu_title_db.objects.raw(SQL)
        # p_m_b = 1
        for b in ps_b:
            p_m_b = b.p_m_b
        
        
        SQL ="select  " 
        SQL += "p_m_idx"
        SQL += ",p_m_b"
        SQL += ",p_m_m" 
        SQL += ",p_m_s"
        SQL += ",p_m_title"
        SQL += ",p_m_indate"
        SQL += ",p_m_YN"
        SQL += ",p_m_asc"        
        SQL += " from psecu_pc_secu_title_db "
        SQL += " where   P_m_YN = 'Y' and p_m_b = 1 and p_m_m = 1 and p_m_s = 0 "
        SQL += " order by p_m_asc desc "

        ps_list_p = pc_secu_title_db.objects.raw(SQL)

        SQL ="select  " 
        SQL += "p_m_idx"
        SQL += ",p_m_b"
        SQL += ",p_m_m" 
        SQL += ",p_m_s"
        SQL += ",p_m_title"
        SQL += ",p_m_indate"
        SQL += ",p_m_YN"
        SQL += ",p_m_asc"        
        SQL += " from psecu_pc_secu_title_db "
        SQL += " where   P_m_YN = 'Y' and p_m_b = 1 and p_m_m = 2 and p_m_s = 0 "
        SQL += " order by p_m_asc desc "

        ps_list_u = pc_secu_title_db.objects.raw(SQL)

        SQL ="select  " 
        SQL += "p_m_idx"
        SQL += ",p_m_b"
        SQL += ",p_m_m" 
        SQL += ",p_m_s"
        SQL += ",p_m_title"
        SQL += ",p_m_indate"
        SQL += ",p_m_YN"
        SQL += ",p_m_asc"        
        SQL += " from psecu_pc_secu_title_db "
        SQL += " where   P_m_YN = 'Y' and p_m_b = 1 and p_m_m = 3 and p_m_s = 0 "
        SQL += " order by p_m_asc desc "

        ps_list_pe = pc_secu_title_db.objects.raw(SQL)        
        username = request.user.get_username()
        useridx = request.user.id
        toDay = time.now().strftime('%Y-%m-%d')
        context ={'ps_list_p':ps_list_p,'ps_list_u':ps_list_u,'ps_list_pe':ps_list_pe,'username':username,'toDay':toDay,'useridx':useridx, 'p_m_b':p_m_b}
    
        return render(request, 'psecu/psecu_form.html',context)
        # 여기에 데이터베이스 저장 로직 추가 가능
    
    # return index(request)

def psecu_detail(request ,p_wb_idx ):
        
        SQL="select A.p_wb_idx" \
            ",A.p_wb_b" \
            ",A.p_wb_wdate" \
            ",A.p_wb_check_userID" \
            ",A.p_wb_check" \
            ",A.p_wb_review_check" \
            ",A.p_wb_review_check_userID  "\
            ",A.p_wb_id_id    "\
            ",B.username as username" \
                
        SQL += " from psecu_pc_work_board_db A left join auth_user B on A.p_wb_id_id = B.id "
        SQL += " where A.p_wb_idx = " + str(p_wb_idx) 
        ps_work = pc_work_board_db.objects.raw(SQL)
        p_m_c_wdate = ""
        for wb in ps_work:
            if wb.p_wb_wdate == None or wb.p_wb_wdate == '':
                p_m_c_wdate = wb.p_wb_indate.strftime('%Y-%m-%d')
            else:
                p_m_c_wdate = wb.p_wb_wdate.strftime('%Y-%m-%d')        

            p_wb_idx = wb.p_wb_idx
            p_wb_b = wb.p_wb_b            
            p_wb_check = wb.p_wb_check
            p_wb_review_check = wb.p_wb_review_check
            p_wb_id_id = wb.p_wb_id_id
            p_username = wb.username



        # p_m_b 가 0 이면 1로 세팅
        if not p_wb_b:
            p_wb_b = 1

        SQL ="select  " 
        SQL += "A.p_m_idx"
        SQL += ",A.p_m_b"
        SQL += ",A.p_m_m" 
        SQL += ",A.p_m_s"
        SQL += ",A.p_m_title"
        SQL += ",A.p_m_indate"
        SQL += ",A.p_m_YN"
        SQL += ",A.p_m_asc"    
        SQL += ",CASE WHEN B.p_m_c_val = 1  THEN '예' ELSE '아니오' END as p_m_c_val "        
        SQL += " from psecu_pc_secu_title_db A left join psecu_pc_secu_ck_db B on A.p_m_idx = B.p_m_idx_id "
        SQL += " where   A.P_m_YN = 'Y' and A.p_m_b = "+str(p_wb_b)+" and A.p_m_m = 1 and A.p_m_s = 0 "
        SQL += " and B.p_wb_idx="+ str(p_wb_idx)
        SQL += " order by A.p_m_asc desc "
        ps_list_p = pc_secu_title_db.objects.raw(SQL)
        # return HttpResponse(SQL)

        SQL ="select  " 
        SQL += "A.p_m_idx"
        SQL += ",A.p_m_b"
        SQL += ",A.p_m_m" 
        SQL += ",A.p_m_s"
        SQL += ",A.p_m_title"
        SQL += ",A.p_m_indate"
        SQL += ",A.p_m_YN"
        SQL += ",A.p_m_asc"    
        SQL += ",CASE WHEN B.p_m_c_val = 1  THEN '예' ELSE '아니오' END as p_m_c_val "        
        SQL += " from psecu_pc_secu_title_db A left join psecu_pc_secu_ck_db B on A.p_m_idx = B.p_m_idx_id "
        SQL += " where   A.P_m_YN = 'Y' and A.p_m_b = "+str(p_wb_b)+" and A.p_m_m = 2 and A.p_m_s = 0 "
        SQL += " and B.p_wb_idx="+ str(p_wb_idx)
        SQL += " order by A.p_m_asc desc "


       

        ps_list_u = pc_secu_title_db.objects.raw(SQL)

        SQL ="select  " 
        SQL += "A.p_m_idx"
        SQL += ",A.p_m_b"
        SQL += ",A.p_m_m" 
        SQL += ",A.p_m_s"
        SQL += ",A.p_m_title"
        SQL += ",A.p_m_indate"
        SQL += ",A.p_m_YN"
        SQL += ",A.p_m_asc"    
        SQL += ",CASE WHEN B.p_m_c_val = 1  THEN '예' ELSE '아니오' END as p_m_c_val "        
        SQL += " from psecu_pc_secu_title_db A left join psecu_pc_secu_ck_db B on A.p_m_idx = B.p_m_idx_id "
        SQL += " where   A.P_m_YN = 'Y' and A.p_m_b = "+str(p_wb_b)+" and A.p_m_m = 3 and A.p_m_s = 0 "
        SQL += " and B.p_wb_idx="+ str(p_wb_idx)
        SQL += " order by A.p_m_asc desc "

        ps_list_pe = pc_secu_title_db.objects.raw(SQL)        
        username = request.user.get_username()
        useridx = request.user.id
        toDay = time.now().strftime('%Y-%m-%d')        
      
        context ={'ps_list_p':ps_list_p
                  ,'ps_list_u':ps_list_u
                  ,'ps_list_pe':ps_list_pe
                  ,'username':username
                  ,'p_m_c_wdate':p_m_c_wdate
                  ,'toDay':toDay
                  ,'useridx':useridx
                  ,'p_wb_idx':p_wb_idx
                  ,'p_wb_check':p_wb_check
                  ,'p_wb_review_check':p_wb_review_check
                  ,'p_wb_id_id':p_wb_id_id
                  ,'p_username':p_username
                  ,'p_wb_b':p_wb_b}
        
        return render(request, 'psecu/psecu_detail.html', context)   


@login_required(login_url='common:login')
def psecu_modify(request, p_wb_idx):   
  
   

    if request.method == 'POST':        
        username = request.user.get_username()
        useridx = request.user.id
        toDay = time.now().strftime('%Y-%m-%d')
        p_m_c_val_list = request.POST.keys()          
        p_m_c_wdate=request.POST.get('p_m_c_wdate')        
        p_wb_idx=request.POST.get('p_wb_idx')


        for key in p_m_c_val_list:            
           
           if key.startswith('psecu_'):                 
                # p_m_val =  key + "_" + request.POST.get(key) + "," + p_m_val
                p_m_idx_id = key.split('_')[1]   
                p_m_val =  request.POST.get(key)
                SQL = "update psecu_pc_secu_ck_db set p_m_c_val = %s,p_m_c_wdate = %s where p_m_idx_id = %s" 
                # return HttpResponse(useridx )
                with connection.cursor() as cursor:
                    cursor.execute(SQL, [p_m_val, p_m_c_wdate, p_m_idx_id]) 

        SQL1 = "update psecu_pc_work_board_db set p_wb_wdate = %s where p_wb_idx = %s  "
        with connection.cursor() as cursor:
            cursor.execute(SQL1, [p_m_c_wdate, p_wb_idx])


        return redirect('psecu:psecu_detail', p_wb_idx=p_wb_idx )
        # SQL1 += " values (%s,%s,%s,%s) "
        # return HttpResponse(useridx )

        # SQL1 = "insert into psecu_pc_work_board_db (p_wb_b, p_wb_id_id, p_wb_indate, p_wb_wdate) "
        # SQL1 += " values (%s,%s,%s,%s) "
        # return HttpResponse(useridx )
        # with connection.cursor() as cursor:
        #     cursor.execute(SQL1, [p_m_b, useridx, toDay, p_m_c_wdate])   

        

        
    else:

        SQL ="select A.p_wb_idx,A.p_wb_b, A.p_wb_wdate, A.p_wb_check, A.p_wb_review_check ,B.username as check_username, C.username as review_check_username "
        SQL +=" from psecu_pc_work_board_db A left join auth_user B on A.p_wb_check_userId = B.id "
        SQL += " left join auth_user C on A.p_wb_review_check_userID = C.id "
        SQL += " where A.p_wb_idx = " + str(p_wb_idx) 
        
        ps_work = pc_work_board_db.objects.raw(SQL)
        p_m_c_wdate = ""
        for wb in ps_work:
            if wb.p_wb_wdate == None or wb.p_wb_wdate == '':
                p_m_c_wdate = wb.p_wb_indate.strftime('%Y-%m-%d')
            else:
                p_m_c_wdate = wb.p_wb_wdate.strftime('%Y-%m-%d') 

            p_wb_idx = wb.p_wb_idx 
            p_wb_check_name = wb.check_username
            p_wb_review_check_name = wb.review_check_username
            p_wb_b= wb.p_wb_b
            p_wb_check = wb.p_wb_check
            p_wb_review_check = wb.p_wb_review_check



        if not p_wb_b:
            p_wb_b = 1

        SQL ="select  " 
        SQL += "A.p_m_idx"
        SQL += ",A.p_m_b"
        SQL += ",A.p_m_m" 
        SQL += ",A.p_m_s"
        SQL += ",A.p_m_title"
        SQL += ",A.p_m_indate"
        SQL += ",A.p_m_YN"
        SQL += ",A.p_m_asc"    
        SQL += ",B.p_m_c_val as p_m_c_val "        
        SQL += " from psecu_pc_secu_title_db A left join psecu_pc_secu_ck_db B on A.p_m_idx = B.p_m_idx_id "
        SQL += " where   A.P_m_YN = 'Y' and A.p_m_b = "+ str(p_wb_b )+ " and A.p_m_m = 1 and A.p_m_s = 0 "
        SQL += " and B.p_m_c_id_id ="+ str(request.user.id)
        SQL += " order by A.p_m_asc desc "

        ps_list_p = pc_secu_title_db.objects.raw(SQL)
  

        SQL ="select  " 
        SQL += "A.p_m_idx"
        SQL += ",A.p_m_b"
        SQL += ",A.p_m_m" 
        SQL += ",A.p_m_s"
        SQL += ",A.p_m_title"
        SQL += ",A.p_m_indate"
        SQL += ",A.p_m_YN"
        SQL += ",A.p_m_asc"    
        SQL += ",B.p_m_c_val as p_m_c_val "        
        SQL += " from psecu_pc_secu_title_db A left join psecu_pc_secu_ck_db B on A.p_m_idx = B.p_m_idx_id "
        SQL += " where   A.P_m_YN = 'Y' and A.p_m_b = "+ str(p_wb_b)+ " and A.p_m_m = 2 and A.p_m_s = 0 "
        SQL += " and B.p_m_c_id_id ="+ str(request.user.id)
        SQL += " order by A.p_m_asc desc "


       

        ps_list_u = pc_secu_title_db.objects.raw(SQL)

        SQL ="select  " 
        SQL += "A.p_m_idx"
        SQL += ",A.p_m_b"
        SQL += ",A.p_m_m" 
        SQL += ",A.p_m_s"
        SQL += ",A.p_m_title"
        SQL += ",A.p_m_indate"
        SQL += ",A.p_m_YN"
        SQL += ",A.p_m_asc"    
        SQL += ",B.p_m_c_val as p_m_c_val "        
        SQL += " from psecu_pc_secu_title_db A left join psecu_pc_secu_ck_db B on A.p_m_idx = B.p_m_idx_id "
        SQL += " where   A.P_m_YN = 'Y' and A.p_m_b = "+ str(p_wb_b)+ " and A.p_m_m = 3 and A.p_m_s = 0 "
        SQL += " and B.p_m_c_id_id ="+ str(request.user.id)
        SQL += " order by A.p_m_asc desc "

        ps_list_pe = pc_secu_title_db.objects.raw(SQL)        
        username = request.user.get_username()
        useridx = request.user.id
        toDay = time.now().strftime('%Y-%m-%d')
        context ={'ps_list_p':ps_list_p
                  ,'ps_list_u':ps_list_u
                  ,'ps_list_pe':ps_list_pe
                  ,'username':username
                  ,'toDay':toDay
                  ,'p_m_c_wdate':p_m_c_wdate
                  ,'useridx':useridx
                  , 'p_wb_idx':p_wb_idx
                  ,'check_username':p_wb_check_name
                  ,'review_check_username':p_wb_review_check_name  
                  ,'p_wb_b':p_wb_b
                  ,'p_wb_check':p_wb_check
                  ,'p_wb_review_check':p_wb_review_check
                  }
        
      

        return render(request, 'psecu/psecu_form.html',context)
    
def psecu_ch_confirm(request):
    if request.method == 'POST':
        p_wb_idx = request.POST.get('p_wb_idx')
        p_m_b = request.POST.get('p_m_b')
        
        useridx = request.user.id
        toDay = time.now().strftime('%Y-%m-%d')

        SQL = "select id,j_gread,j_name,j_yn,j_id_id from board_jik_gread where j_id_id=" + str(useridx) + ""
        ps_jik = Jik_gread.objects.raw(SQL)
        jik_gread = ""  
        for jk in ps_jik:
            jik_gread = jk.j_gread

        
        if jik_gread == 2 :
         # Update the work board check status
            SQL2 = "select p_wb_idx,p_wb_b,p_wb_indate,p_wb_wdate,p_wb_review_check,p_wb_check from psecu_pc_work_board_db where p_wb_idx = %s "
            ps_wb = pc_work_board_db.objects.raw(SQL2, [p_wb_idx])
            p_wb_check = ''    
            p_check = ''  
            for wb in ps_wb:
                p_wb_check = wb.p_wb_check
            
            if p_wb_check == 'N':
                p_check = 'Y'
            else:
                p_check = 'N'           
            
            SQL1= "update psecu_pc_work_board_db set p_wb_check = %s,p_wb_check_userID = %s where p_wb_idx = %s "             
            with connection.cursor() as cursor:
                cursor.execute(SQL1, [p_check, useridx, p_wb_idx])
            #로그기록으로남기기

            # SQL3 = "insert into psecu_pc_secu_cf_db (p_m_idx_id, p_m_cf_val, p_m_c_id_id, p_m_jik_id_id, p_m_cf_indate) values (%s,%s,%s,%s,%s)"
            # with connection.cursor() as cursor:
            #     cursor.execute(SQL3, [p_m_c_idx, p_check, useridx, jik_gread, toDay])
            # str_text = str(p_wb_check)+'/'+str(p_check)+'/'+str(p_wb_idx)
            result = {'p_check': p_check}
            return HttpResponse(json.dumps(result), content_type="application/json")                      
            # return HttpResponse('SQL','SQL1')
        else:
            result = {'p_check': 'gf'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'p_check': 'fail'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    


    
@login_required(login_url='common:login')
def psecu_review_confirm(request):
    if request.method == 'POST':
        p_wb_idx = request.POST.get('p_wb_idx')            
        
        useridx = request.user.id
        

        SQL = "select id,j_gread,j_name,j_yn,j_id_id from board_jik_gread where j_id_id=" + str(useridx) + ""
        ps_jik = Jik_gread.objects.raw(SQL)
        jik_gread = ""  
        for jk in ps_jik:
            jik_gread = jk.j_gread

        
        if jik_gread == 3 :
         # Update the work board check status
            SQL2 = "select p_wb_idx,p_wb_b,p_wb_indate,p_wb_wdate,p_wb_review_check,p_wb_check from psecu_pc_work_board_db where p_wb_idx = %s "
            ps_wb = pc_work_board_db.objects.raw(SQL2, [p_wb_idx])
            p_wb_review_check = ''    
            p_check = ''  
            for wb in ps_wb:
                p_wb_review_check = wb.p_wb_review_check
            
            if p_wb_review_check == 'N':
                p_check = 'Y'
            else:
                p_check = 'N'           
            

            # 검토자가 확인을 하면 담당자는 자동으로 확인처리
            SQL1= "update psecu_pc_work_board_db set p_wb_review_check = %s,p_wb_review_check_userID = %s,p_wb_check = %s ,p_wb_check_userID = %s where p_wb_idx = %s "             
            with connection.cursor() as cursor:
                cursor.execute(SQL1, [p_check, useridx, p_check, useridx, p_wb_idx])
            #로그기록으로남기기

            result = {'p_check': p_check}
            return HttpResponse(json.dumps(result), content_type="application/json")                      
        else:
            result = {'p_check': 'gf'}
            return HttpResponse(json.dumps(result), content_type="application/json")
            
    else:
        result = {'p_check': 'fail'}
        return HttpResponse(json.dumps(result), content_type="application/json")