from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect,resolve_url
from .models import Q_board,Category
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



def b_delete(request,category_id,qboard_id):

    qboard = get_object_or_404(Q_board,pk=qboard_id)
    if request.user != qboard.b_name:
        message = '삭제권한이 없습니다'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")        
        # return redirect('pybo:detail',category_id=category_id,question_id=question.id)
    qboard.delete()
    return redirect('board:b_list',category_id=category_id)


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
    