from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from pybo.models import Question,Answer,Catogory
from pybo.models import Qcomment,Acomment
from mt.models import company_info, subject_db
from django.db.models import Q


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
    return render(request, 'manager/index.html',context)

def list(request,category_id):
    page = request.GET.get('page', '1')  # 페이지    
    kw = request.GET.get('kw','')    
    # category_id = request.GET.get('category_id',1)
    category = get_object_or_404(Catogory,pk=category_id)
    # category_list = Catogory.objects.all()
    question_list = Question.objects.filter(category=category.id).order_by('-create_date')    

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | 
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw) 
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    if category_id == 1:
        b_title ="Q & A"
    elif category_id == 2:
        b_title ="Free Board"    
    elif category_id == 3:
        b_title ="Notice"

    context ={'question_list':page_obj,'page':page,'kw':kw,'category_id':category.id,'b_title':b_title }
    

    return render(request,'manager/mpybo/question_list.html',context)


    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


def detail(request,question_id,category_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id)
    
    page_a=request.GET.get('dpage', '1')
    answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    paginator_a=Paginator(answer_list, 3)
    page_obj_a=paginator_a.get_page(page_a)
    
    qcomment_list =Qcomment.objects.filter(question=question).order_by('-create_date')
    acomment_list =Acomment.objects.filter(answer_id__in=answer_list).order_by('-create_date')
    # # acomment_list =Acomment.objects.all()


    context ={'question':question,'answer_list': page_obj_a,'qcomment_list':qcomment_list,'acomment_list':acomment_list,'category_id':category_id }
    # context ={'question':question}
    return render(request,'manager/mpybo/question_detail.html',context)


def categoryView(request):
    # category_posts = Catogory.objects.filter(category=category_name)
    categories = Catogory.objects.all()
    return render(
        request,
        "pybo/category.html",
        {
            # "category_name": category_name,
            # "category_posts": category_posts,
            "categories": categories,
        },
    )