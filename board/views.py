from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect,resolve_url
from .models import Q_board,Category
from .models import Jik_gread,Approve
from django.db.models import Q
from django.utils import timezone
from .forms import QForm
import os
from django.conf import settings
from django.http import HttpResponse
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote
from django import forms # 추가
from django_summernote.widgets import SummernoteWidget # 추가
import requests
# from pyhwpx import Hwp
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
# import pyhwpx

form_article = forms.modelform_factory( # 글 작성과 편집에 사용하는 form
    Q_board, # form에 사용되는 model
    forms.ModelForm, # 기본 form
    fields='__all__', # form에서 편집 가능한 필드 목록
    widgets={'b_content': SummernoteWidget()} # content field에 summernote editor 적용
)

# Create your views here.

@login_required(login_url='common:login')
def b_create(request,category_id):
    category =get_object_or_404(Category,pk=category_id)
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            qboard = form.save(commit=False)
            qboard.b_name = request.user
            qboard.b_create_date = timezone.now()
            qboard.b_gubun = category
            qboard.b_cnt = 0 
            qboard.b_status = 0 
            qboard.b_link_one = request.POST['b_link_one']
            qboard.b_link_two = request.POST['b_link_two']
            qboard.b_file_one = request.FILES.get('b_file_one') 
            qboard.b_file_two = request.FILES.get('b_file_two') 
            qboard.b_file_three = request.FILES.get('b_file_three') 
            qboard.save()
            return redirect('board:b_list',category_id=category.id)
    else:
        form = QForm()
    context = {'form': form,'category_name':category.name}
    return render(request, 'board/board_form.html', context)


def b_list(request,category_id):
    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')    
    # category_id = request.GET.get('category_id',1)
    category = get_object_or_404(Category,pk=category_id)
    # category_list = Catogory.objects.all()
    q_list = Q_board.objects.filter(b_gubun=category.id).order_by('-b_create_date')    

    if kw:
        q_list = q_list.filter(
            Q(b_subject__icontains=kw) | 
            Q(b_content__icontains=kw) 
           
        ).distinct()
    paginator = Paginator(q_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context ={'q_list':page_obj,'page':page,'category_id':category.id }

    return render(request,'board/board_list.html',context)


    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


    

@login_required(login_url='common:login')
def b_detail(request,qboard_id,category_id):
    # question = Question.objects.get(id=question_id)
    qboard = get_object_or_404(Q_board,pk=qboard_id)
    b_err_gubun_name = ''
    if qboard.b_err_gubun == 1 :
        b_err_gubun_name = 'LMS 장애'
    elif qboard.b_err_gubun == 2 :
        b_err_gubun_name = '서버 장애'
    elif qboard.b_err_gubun == 3 :
        b_err_gubun_name = '개발 장애'
    else :
        b_err_gubun_name = '기타 장애'


    qboard.b_err_gubun = b_err_gubun_name

   


    # page_a=request.GET.get('dpage', '1')
    # answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    # paginator_a=Paginator(answer_list, 3)
    # page_obj_a=paginator_a.get_page(page_a)
    
    # qcomment_list =Qcomment.objects.filter(question=question).order_by('-create_date')
    # acomment_list =Acomment.objects.filter(answer_id__in=answer_list).order_by('-create_date')
    # # acomment_list =Acomment.objects.all()


    # context ={'qboard':qboard,'answer_list': page_obj_a,'qcomment_list':qcomment_list,'acomment_list':acomment_list,'category_id':category_id }
    context ={'qboard':qboard,'category_id':category_id }
    # context ={'question':question}
    return render(request,'board/board_detail.html',context)


@login_required(login_url='common:login')
def b_modify(request, category_id,qboard_id):
    qboard = get_object_or_404(Q_board, pk=qboard_id)
    category = get_object_or_404(Category,pk=category_id)
    if request.user != qboard.b_name:
        #messages.error(request, '수정권한이 없습니다')
        return redirect('board:b_detail', qboard_id=qboard.id)
    if request.method == "POST":
        form = QForm(request.POST, instance=qboard)
        if form.is_valid():
            qboard = form.save(commit=False)
            # question.modify_date = timezone.now()  # 수정일시 저장
           
            qboard.b_create_date = timezone.now()
            qboard.b_gubun = category
            qboard.b_cnt = 0 
            qboard.b_status = 0 
            
            


            if request.FILES.get('b_file_one') :
                qboard.b_file_one.delete(save=False)
                qboard.b_file_one = request.FILES.get('b_file_one') 
                
            if request.FILES.get('b_file_two')  :
                qboard.b_file_two.delete(save=False)
                qboard.b_file_two = request.FILES.get('b_file_two') 

            if request.FILES.get('b_file_three')  :
                qboard.b_file_three.delete(save=False)                
                qboard.b_file_three = request.FILES.get('b_file_three') 

            qboard.save()
            return redirect('board:b_detail',category_id=category_id, qboard_id=qboard.id)
    else:
        form = QForm(instance=qboard)   
        
    context = {'form': form,'category_name':category.name,'qboard' : qboard }
    return render(request, 'board/board_form.html', context)


@login_required(login_url='common:login')
def b_delete(request,category_id,qboard_id):

    qboard = get_object_or_404(Q_board,pk=qboard_id)
    if request.user != qboard.b_name:
        message = '삭제권한이 없습니다'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")        
        # return redirect('pybo:detail',category_id=category_id,question_id=question.id)
    qboard.delete()
    return redirect('board:b_list',category_id=category_id)

@login_required(login_url='common:login')
def file_download(request):
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    # return HttpResponse()
    file_name = os.path.basename(path) 
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        encoded_filename = quote(file_name.encode('utf-8'))        
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % encoded_filename
        
        return response
    else:
        message = '알 수 없는 오류가 발행하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")


@login_required(login_url='common:login')
def approve_list(request):
    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')    
    # category_id = request.GET.get('category_id',2)
    # category = get_object_or_404(Category,pk=category_id)
    # category_list = Catogory.objects.all()

    SQL = "SELECT A.* "
    SQL += "	  ,CASE WHEN IFNULL(B.A_APPROVE,'N') = 'N' THEN  '검토중' ELSE '검토확인' END   AS examine "
    SQL += "	  ,CASE WHEN IFNULL(C.A_APPROVE,'N') ='N' THEN '확인중' ELSE '확인완료' END  AS che  "
    SQL += " FROM BOARD_Q_BOARD A "
    SQL += " LEFT JOIN BOARD_APPROVE B ON A.ID=B.A_BOARD_ID AND B.A_JIK_ID=2 "
    SQL += " LEFT JOIN BOARD_APPROVE C ON A.ID = C.A_BOARD_ID AND C.A_JIK_ID=3 "
    if kw:
        SQL += " WHERE A.B_SUBJECT LIKE '%%"+kw+"%%' OR A.B_CONTENT LIKE '%%"+kw+"%%' "
    SQL += " ORDER BY A.B_CREATE_DATE DESC "

    # SQL = " SELECT  A.* "
    # SQL += ",CASE WHEN IFNULL((SELECT a_approve from board_approve where a_jik_id=2 and a_board_id=a.id),'N') ='N' THEN '검토중' ELSE '검토완료' END  as examine "
    # SQL += ",CASE WHEN  IFNULL((SELECT a_approve from board_approve where a_jik_id=3 and a_board_id=a.id),'N') ='N' THEN '확인중' ELSE '확인완료' END  as che "
    # SQL += "FROM BOARD_Q_BOARD A "
    # if kw:
    #     SQL += " WHERE A.B_SUBJECT LIKE '%%"+kw+"%%' OR A.B_CONTENT LIKE '%%"+kw+"%%' "

    # SQL += "ORDER BY B_CREATE_DATE DESC "
    a_list = Q_board.objects.raw(SQL)
    # a_list = Q_board.objects.filter(pk=Approve).order_by('-b_create_date')    

    # if kw:
    #     a_list = a_list.filter(
    #         Q(b_subject__icontains=kw) | 
    #         Q(b_content__icontains=kw) 
           
    #     ).distinct()
    paginator = Paginator(a_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context ={'a_list':page_obj,'page':page}

    return render(request,'board/approve_list.html',context)

@login_required(login_url='common:login')
def a_detail(request,aboard_id):
    # question = Question.objects.get(id=question_id)
    qboard = get_object_or_404(Q_board,pk=aboard_id) # 게시글 정보 가져오기
    b_err_gubun_name = ''
    if qboard.b_err_gubun == 1 :
        b_err_gubun_name = 'LMS 장애'
    elif qboard.b_err_gubun == 2 :
        b_err_gubun_name = '서버 장애'
    elif qboard.b_err_gubun == 3 :
        b_err_gubun_name = '개발 장애'
    else :
        b_err_gubun_name = '기타 장애'


    qboard.b_err_gubun = b_err_gubun_name
    J_jik = get_object_or_404(Jik_gread,j_id=request.user)
    alist= Approve.objects.filter(a_board=aboard_id) # 승인자 정보 가져오기
    
    examine='N'
    check='N'  
    j_jik = J_jik.j_gread 
    if alist.count() <1 : # 승인자가 없는 경우
        examine='N'
        check='N'
    else :
        for a in alist: #승인건은 2건만 나와야 함 검토자와  확인자
            if a.a_jik_id ==2 : # 승인자 직급이 2인 경우
                if a.a_approve=='Y': # 승인여부가 Y인 경우
                    examine='Y'                           
            if a.a_jik_id==3 : # 승인자 직급이 3인 경우
                if a.a_approve=='Y': # 승인여부가 Y인 경우
                    check='Y'
              
                  
   
    # page_a=request.GET.get('dpage', '1')
    # answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    # paginator_a=Paginator(answer_list, 3)
    # page_obj_a=paginator_a.get_page(page_a)
    
    # qcomment_list =Qcomment.objects.filter(question=question).order_by('-create_date')
    # acomment_list =Acomment.objects.filter(answer_id__in=answer_list).order_by('-create_date')
    # # acomment_list =Acomment.objects.all()


    # context ={'qboard':qboard,'answer_list': page_obj_a,'qcomment_list':qcomment_list,'acomment_list':acomment_list,'category_id':category_id }
    context ={'qboard':qboard, 'examine':examine, 'check':check ,'j_jik':j_jik,'aboard_id':aboard_id}
    # context ={'question':question}
    return render(request,'board/approve_detail.html',context)

@login_required(login_url='common:login')
def ajax_sungin(request):
    if request.method == "POST":
        gubun = request.POST.get('gubun')
        if gubun == 'examine': # 검토자 승인
            jik = 2
        elif gubun == 'check': # 확인자 승인
            jik = 3

        qboard_id = request.POST.get('qboard_id')
        approve = request.POST.get('approve')

        # qboard_id = request.POST['qboard_id']
        # approve = request.POST['approve']
        qboard = get_object_or_404(Q_board,pk=qboard_id) # 게시글 정보 가져오기
        J_jik = get_object_or_404(Jik_gread,j_id=request.user, j_gread= jik)
        a_approve='N'
        if approve=='Y':
            a_approve='Y'
        else:
            a_approve='N'
        
        try:
            approve_record = Approve.objects.get(a_board=qboard, a_jik=J_jik.j_gread) # 기존 승인 기록이 있는지 확인
            approve_record.a_approve = a_approve # 승인 상태 업데이트
            approve_record.a_approve_date = timezone.now() # 승인 날짜 업데이트
            approve_record.save()
        except Approve.DoesNotExist:
            new_approve = Approve(
                a_board=qboard,
                a_jik=J_jik.j_gread,
                a_approve=a_approve,
                a_approve_date=timezone.now()
            )
            new_approve.save()
        
        return HttpResponse("Success")
    return HttpResponse("Invalid request")

    # gubun = request.POST.get('gubun')
    # if gubun == 'examine': # 검토자 승인
    #     jik = 2
    # elif gubun == 'check': # 확인자 승인
    #     jik = 3


    # J_jik = get_object_or_404(Jik_gread,j_id=request.user)
    # gubun = request.POST['qboard_id']
    # return HttpResponse(request.user)


@login_required(login_url='common:login')
def approve_print(request,qboard_id):
    pass

    # hwp = Hwp()
    
    # path = 'hwpex/LMS 개발 제안보고서.hwp'
    # file_path = os.path.join(settings.MEDIA_ROOT, path)


    # oldFile = hwp.Open(file_path)
    # # file_name =f"{gi_su}수_수료보고_{company_name}.hwp"
    
    


    # SQL = "SELECT A.* "
    # SQL += "	  ,CASE WHEN IFNULL(B.A_APPROVE,'N') = 'N' THEN  '검토중' ELSE '검토확인' END   AS examine "
    # SQL += "	  ,CASE WHEN IFNULL(C.A_APPROVE,'N') ='N' THEN '확인중' ELSE '확인완료' END  AS che  "
    # SQL += " FROM BOARD_Q_BOARD A "
    # SQL += " LEFT JOIN BOARD_APPROVE B ON A.ID=B.A_BOARD_ID AND B.A_JIK_ID=2 "
    # SQL += " LEFT JOIN BOARD_APPROVE C ON A.ID = C.A_BOARD_ID AND C.A_JIK_ID=3 "    
    # SQL += " WHERE A.id = %s " % qboard_id
    # qboard = Q_board.objects.raw(SQL)
    # b_date = qboard[0].b_create_date.strftime('%Y-%m-%d')
    # b_name = qboard[0].b_name.username  
    # b_subject = qboard[0].b_subject
    # # url = "board/approve_content.html"
    # # url = "http://127.0.0.1:8000/board/approve_list/approve_content/" + str(qboard_id) + "/"
    # # response = requests.get(url)
    # # b_content =  qboard[0].b_content
    # # b_content =  BeautifulSoup(response.text, 'html.parser').get_text()
    # b_content =  BeautifulSoup(qboard[0].b_content, 'html.parser')
    
    # # b_content =  qboard[0].b_content  

    # examine = '검토중'
    # che = '확인중'  
    # file_name =f"개발 제안보고서_{b_date}.hwp"
    # hwp.put_field_text("b_date", b_date)
    # hwp.put_field_text("examine", examine)
    # hwp.put_field_text("che", che)
    # hwp.put_field_text("subject", b_subject)
    # # hwp.put_field_text("contents", BeautifulSoup(b_content,'html.parser').get_text())
    # # hwp.put_field_text("contents", b_content)
    # hwp.MoveToField("contents")
    # hwp.InsertPicture(settings.MEDIA_ROOT + '/img/screenshot3.png', 100, 30)  # 이미지 삽입
    # hwp.SaveAs(file_name,format="HTML+", split_page=False) 
    
    # hwp.close()
    # context ={'qboard':qboard[0]}     
    # # return render(request,'board/approve_print.html',context)
    # # return render(request,'board/approve_print.html',context)
    # return FileResponse(open(file_name, 'rb'), as_attachment=True, filename=file_name)


    
@login_required(login_url='common:login')
def approve_content(request,qboard_id):        
    SQL = "SELECT A.id,A.b_content "    
    SQL += " FROM BOARD_Q_BOARD A "      
    SQL += " WHERE A.id = %s " % qboard_id
    qboard = Q_board.objects.raw(SQL)    
    
    # b_content =  qboard[0].b_content  
    
    context ={'qboard':qboard[0]}         
    return render(request,'board/approve_content.html',context)    
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    

