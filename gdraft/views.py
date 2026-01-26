import re
from unittest import result
from urllib import request
from django import forms
from django.shortcuts import get_object_or_404, render
from .models import Gdraft_db,Gdraft_log,Gdraft_status
from board.models import Jik_gread 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime as time, timezone
from django.http import HttpResponse
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.shortcuts import redirect
from django.core import serializers
import json
from .forms import gdrform, selectform
from django.forms import modelform_factory
from django_summernote.widgets import SummernoteWidget
from board.models import Jik_gread




# Create your views here.

form_article = forms.modelform_factory( # 글 작성과 편집에 사용하는 form
    Gdraft_db, # form에 사용되는 model
    forms.ModelForm, # 기본 form
    fields='__all__', # form에서 편집 가능한 필드 목록
    widgets={'dr_content': SummernoteWidget()} # content field에 summernote editor 적용
)


@login_required(login_url='common:login')
def login_gik_gread(user_id):
    SQL = "select j_gread from board_jik_gread where j_id_id = "+str(user_id)
    result=Jik_gread.objects.raw(SQL)   

    return result[0] if result else None
    


def index(request):
    
    # return HttpResponse(request.user.id)

    # 먼저 직급 체크 부터 한다.
    SQL = "select id,j_gread from board_jik_gread where j_id_id = "+str(request.user.id)
    result=Jik_gread.objects.raw(SQL)   
    
    user_jik_gread = result[0].j_gread if result else None

    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')

    SQL = "select  dr_idx"     
    SQL +=",A.dr_no"
    SQL +=",A.dr_date"
    SQL +=",A.dr_title"
    SQL +=",A.dr_content"
    SQL +=",A.dr_attachfile"
    SQL +=",A.dr_indate"
    SQL +=",A.dr_save_status"
    SQL +=",A.dr_status"
    SQL +=",A.dr_id_id"
    SQL +=",B.username username"
    SQL +=",ifNULL(C.drs_status, '결재대기') drs_status_C" # 담당자
    SQL +=",ifNULL(D.drs_status, '결재대기') drs_status_D"  # 임원급
    SQL +=",C.drs_comment drs_comment_C"
    SQL +=",D.drs_comment drs_comment_D"
    SQL +=" from gdraft_gdraft_db A left join auth_user B on A.dr_id_id=B.id "
    SQL +=" left join gdraft_gdraft_status C on A.dr_idx=C.dr_idx_id and C.drs_jik=2  "
    SQL +=" left join gdraft_gdraft_status  D on A.dr_idx =D.dr_idx_id and D.drs_jik=3 "  # 담당자
    if kw:
        SQL +=" where A.dr_title like '%"+kw+"%' or A.dr_content like '%"+kw+"%' "
    
    # return HttpResponse(SQL)
    dr_list = Gdraft_db.objects.raw(SQL)
    paginator = Paginator(dr_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
 
    context ={'dr_list':page_obj,'page':page,'kw':kw ,'user_jik_gread': str(user_jik_gread)}

    return render(request, 'gdraft/index.html',context)

@login_required(login_url='common:login')
def gdraft_submit(request):

    if request.method == "POST":
        form = gdrform(request.POST, request.FILES)
        if form.is_valid():
            gdraft = form.save(commit=False)
            gdraft.dr_id_id = request.user.id
            gdraft.dr_no = request.POST['dr_no']
            gdraft.dr_date = request.POST['dr_date']
            gdraft.dr_title = request.POST['dr_title']
            gdraft.dr_status = '결재대기'           
            gdraft.dr_attachfile = request.FILES.get('dr_attachfile')
            gdraft.dr_indate = time.now().date()
            gdraft.dr_save_status = request.POST['dr_save_status']          
            gdraft.save()
            return redirect('gdraft:index')
        else:
            return render(request,'gdraft/gdraft_form.html', {'form': form})

    else:
        SQL = "select  max(dr_no) as max_dr_no from gdraft_gdraft_db"
        cursor = connection.cursor()
        cursor.execute(SQL)
        row = cursor.fetchone()
        toYear = time.now().year
        
        if row[0] == None:
            max_dr_no = 'DR00001_' +str(toYear)  
        else:
            max_dr_no = 'DR' + str(int(row[0][2:7])+1).zfill(5) + '_' + str(toYear)

        form = gdrform(initial={'dr_no': max_dr_no} )
        return render(request,'gdraft/gdraft_form.html', {'form': form})    
    

    
def gdraft_detail(request, dr_idx):
    # gdraft = get_object_or_404(Gdraft_db, pk=dr_idx)    
    # user_jik_gread = jik_check(request.user.id)
    SQL = "select id,j_gread from board_jik_gread where j_id_id = "+str(request.user.id)
    result=Jik_gread.objects.raw(SQL)   
    
    user_jik_gread = result[0].j_gread if result else None



    SQL = "select  dr_idx"     
    SQL +=",A.dr_no"
    SQL +=",A.dr_date"
    SQL +=",A.dr_title"
    SQL +=",A.dr_content"
    SQL +=",A.dr_attachfile"
    SQL +=",A.dr_indate"
    SQL +=",A.dr_save_status"
    SQL +=",A.dr_status"
    SQL +=",A.dr_id_id"
    SQL +=",B.username username"
    SQL +=",ifNULL(C.drs_status, '결재대기') drs_status_C" # 담당자
    SQL +=",ifNULL(D.drs_status, '결재대기') drs_status_D"  # 임원급
    SQL +=",ifNULL(C.drs_comment, '') drs_comment_C"
    SQL +=",ifNULL(D.drs_comment, '') drs_comment_D"
    SQL +=" from gdraft_gdraft_db A left join auth_user B on A.dr_id_id=B.id "
    SQL +=" left join gdraft_gdraft_status C on A.dr_idx=C.dr_idx_id and C.drs_jik=2  "
    SQL +=" left join gdraft_gdraft_status  D on A.dr_idx =D.dr_idx_id and D.drs_jik=3 "  # 담당자

    SQL +=" where A.dr_idx="+str(dr_idx)

    # return HttpResponse(SQL)
    gdraft = Gdraft_db.objects.raw(SQL)  

    t_dts_status=gdraft[0].drs_status_D
    if user_jik_gread ==2:
        dts_status = gdraft[0].drs_status_C 
        dts_comment = gdraft[0].drs_comment_C
       
    elif user_jik_gread ==3:
        dts_status = gdraft[0].drs_status_D 
        dts_comment = gdraft[0].drs_comment_D
       
    else:
        dts_status = ''
        dts_comment = ''




    context = {'gdraft': gdraft[0], 'user_jik_gread': int(user_jik_gread), 'dts_status': dts_status, 'dts_comment': dts_comment, 't_dts_status': t_dts_status}
    return render(request, 'gdraft/gdraft_detail.html', context)

def download(request):
    file_path = request.GET.get('path')
    fs = FileSystemStorage()
    filename = file_path.split('/')[-1]
    response = FileResponse(fs.open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required(login_url='common:login')
def gdraft_modify(request, dr_idx): 
    gdraft = get_object_or_404(Gdraft_db, pk=dr_idx)    
    if request.method == "POST":
        form = gdrform(request.POST, request.FILES, instance=gdraft)
        if form.is_valid():
            gdraft = form.save(commit=False)
            gdraft.dr_id_id = request.user.id
            gdraft.dr_no = request.POST['dr_no']
            gdraft.dr_date = request.POST['dr_date']
            gdraft.dr_title = request.POST['dr_title']     
            if request.FILES.get('dr_attachfile') :
                gdraft.dr_attachfile.delete(save=False)
                gdraft.dr_attachfile = request.FILES.get('dr_attachfile')                   
            gdraft.dr_indate = time.now().date()
            gdraft.dr_save_status = request.POST['dr_save_status']          
            gdraft.save()
            return redirect('gdraft:gdraft_detail', dr_idx=gdraft.dr_idx)
        else:
           
            return render(request,'gdraft/gdraft_form.html', {'form': form})

    else:
        form = gdrform(instance=gdraft)
        return render(request,'gdraft/gdraft_form.html', {'form': form, 'gdraft': gdraft})
    
@login_required(login_url='common:login')
def gdraft_delete(request, dr_idx):
    gdraft = get_object_or_404(Gdraft_db, pk=dr_idx)    
    gdraft.delete()    
    return redirect('gdraft:index') 

def gdraft_status(request):
    form = selectform()
    return render(request, 'gdraft/gdraft_status.html', {'form': form})


def gstatus_submit(request):
    if request.method == "POST":
        form = selectform(request.POST)
        if form.is_valid():
            # dr_status = form.cleaned_data['dr_status']
            # 여기에 dr_status 값을 처리하는 로직을 추가하세요.
            # 예: 데이터베이스에 저장하거나 다른 작업 수행
            dr_status = request.POST['dr_status']
            gdraft_id = int(request.POST['dr_idx'])
            Jik_gread = int(request.POST['jik_gread'])
            drs_comment = request.POST['drs_comment']
            SQL_JIK = "select id,j_name,j_gread  from board_jik_gread where j_id_id=%s"
            cursor = connection.cursor()
            cursor.execute(SQL_JIK, [request.user.id])

            row_jik = cursor.fetchone()
            if row_jik:
                user_jik_name = row_jik[1]
                user_jik_gread = row_jik[2]

            # 권한 체크
            # 권한자의 등급을 보고 처리
            if (int(user_jik_gread) != Jik_gread):
                result = {'msg': '권한이 없습니다.'}
                return HttpResponse(json.dumps(result), content_type="application/json")
            


            SQL = "select drs_idx,dr_idx_id  from gdraft_gdraft_status where dr_idx_id="+str(gdraft_id)+" and drs_jik="+str(user_jik_gread)
            result=Gdraft_status.objects.raw(SQL)   
            row = result[0].drs_idx if result else None

            if row is None:
                gdraft_status = Gdraft_status()
                gdraft_status.drs_status = dr_status
                gdraft_status.dr_idx_id = gdraft_id
                gdraft_status.drs_id_id = request.user.id
                gdraft_status.drs_jik = int(user_jik_gread)  # 여기에 적절한 직급 ID를 설정하세요.
                gdraft_status.drs_date = time.now().date()
                gdraft_status.drs_comment = drs_comment
                gdraft_status.save()
            else:
                
                gdraft_status = Gdraft_status.objects.get(dr_idx_id=gdraft_id, drs_jik=int(user_jik_gread))
                gdraft_status.drs_status = dr_status
                gdraft_status.drs_date = time.now().date()
                gdraft_status.drs_comment = drs_comment
                gdraft_status.save()            


            if (Jik_gread==3) : #최종 결재자
                gdraft = Gdraft_db.objects.get(dr_idx=gdraft_id)
                gdraft.dr_status = dr_status
                gdraft.save()
           

            # 로그 남기기
            gdraft_log = Gdraft_log()
            gdraft_log.dr_idx_id = gdraft_id
            gdraft_log.drl_id_id = request.user.id
            gdraft_log.drl_date = time.now().date()
            gdraft_log.drl_action = dr_status
           
            gdraft_log.save()


            result = {'msg': '변경이 되었습니다.'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        form = selectform()
    return render(request, 'gdraft/gdraft_status.html', {'form': form})

def gdraft_print(request, dr_idx):

    SQL = "select  dr_idx"     
    SQL +=",A.dr_no"
    SQL +=",A.dr_date"
    SQL +=",A.dr_title"
    SQL +=",A.dr_content"
    SQL +=",A.dr_attachfile"
    SQL +=",A.dr_indate"
    SQL +=",A.dr_save_status"
    SQL +=",A.dr_status"
    SQL +=",A.dr_id_id"
    SQL +=",B.username username"
    SQL +=",ifNULL(C.drs_status, '결재대기') drs_status_C" # 담당자
    SQL +=",ifNULL(D.drs_status, '결재대기') drs_status_D"  # 임원급
    SQL +=",ifNULL(C.drs_comment, '') drs_comment_C"
    SQL +=",ifNULL(D.drs_comment, '') drs_comment_D"
    SQL +=" from gdraft_gdraft_db A left join auth_user B on A.dr_id_id=B.id "
    SQL +=" left join gdraft_gdraft_status C on A.dr_idx=C.dr_idx_id and C.drs_jik=2  "
    SQL +=" left join gdraft_gdraft_status  D on A.dr_idx =D.dr_idx_id and D.drs_jik=3 "  # 담당자

    SQL +=" where A.dr_idx="+str(dr_idx)

    # return HttpResponse(SQL)
    gdraft = Gdraft_db.objects.raw(SQL)  
    context = {'gdraft': gdraft[0]}   
    
    return render(request, 'gdraft/gdraft_print.html', context)
    
    # return render(request, 'gdraft/gdraft_print.html', context)
    # return HttpResponse(pdf, content_type='application/pdf')


def render_to_pdf(template_src, context_dict):
    pass

