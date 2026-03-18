from multiprocessing import connection
from django.db import connection

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from requests import request
from django.db.models import  Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from f_board.models import F_board
from f_board.forms import FForm
from urllib.parse import quote
import os
# Create your views here.
def f_detail(request, f_board_id):
    sqlup="update f_board_f_board set f_cnt = f_cnt + 1 where f_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(sqlup, [f_board_id])


    f_board = get_object_or_404(F_board, pk=f_board_id)

    context = {'f_board':f_board}
    return render(request, 'f_board/f_detail.html', context)




@login_required(login_url='common:login')
def f_create(request):
    if request.method == 'POST':
        form = FForm(request.POST)
        if form.is_valid():
            f_board = form.save(commit=False)
            f_board.f_name = request.user
            f_board.f_create_date = timezone.now()
            f_board.f_title = request.POST['f_title']
            f_board.f_contents = request.POST['f_contents']
            f_board.f_yn = 'Y'
            f_board.f_cnt = 0
            f_board.f_d_cnt = 0
            f_board.f_file_one = request.FILES.get('f_file_one') 
            f_board.f_file_two = request.FILES.get('f_file_two') 
            f_board.f_file_three = request.FILES.get('f_file_three') 
            f_board.save()
            return redirect('f_board:f_list')
    else:
        form = FForm()
    context = {'form': form}
    return render(request, 'f_board/f_form.html', context)



def f_list(request):
    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')    
    
    f_list = F_board.objects.filter().order_by('-f_create_date')    

    if kw:
        f_list = f_list.filter(
            Q(f_title__icontains=kw) | 
            Q(f_contents__icontains=kw) 
           
        ).distinct()
    paginator = Paginator(f_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context ={'f_list':page_obj,'page':page,'kw':kw,} 

    
    return render(request, 'f_board/f_list.html', context)



@login_required(login_url='common:login')
def f_modify(request, f_board_id):
    f_board = get_object_or_404(F_board, pk=f_board_id)
    if request.method == "POST":
        form = FForm(request.POST, request.FILES, instance=f_board)        

        if form.is_valid():
            f_board = form.save(commit=False)
            f_board.f_name = request.user
            f_board.f_create_date = timezone.now()
            #업로든 된 파일이 없으면 기존 파일 유지
            if request.FILES.get('f_file_one') or request.POST.get('f_file_one_clear') == 'on':
                if f_board.f_file_one:
                    if os.path.isfile(f_board.f_file_one.path):
                        os.remove(f_board.f_file_one.path)
                f_board.f_file_one = request.FILES.get('f_file_one') 
            if request.FILES.get('f_file_two') or request.POST.get('f_file_two_clear') == 'on':
                if f_board.f_file_two:
                    if os.path.isfile(f_board.f_file_two.path):
                        os.remove(f_board.f_file_two.path)  
                f_board.f_file_two = request.FILES.get('f_file_two') 
            if request.FILES.get('f_file_three') or request.POST.get('f_file_three_clear') == 'on':
                if f_board.f_file_three:
                    if os.path.isfile(f_board.f_file_three.path):
                        os.remove(f_board.f_file_three.path)
                f_board.f_file_three = request.FILES.get('f_file_three')         

            f_board.save()
            return redirect('f_board:f_detail', f_board_id=f_board.f_id)
    else:
        form = FForm(instance=f_board)
    context = {'form': form, 'f_board': f_board}
    return render(request, 'f_board/f_form.html', context)


@login_required(login_url='common:login')
def f_delete(request, f_board_id):
    f_board = get_object_or_404(F_board, pk=f_board_id)
    f_board.delete()
    return redirect('f_board:f_list') 


@login_required(login_url='common:login')
def f_download(request):    
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