from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from pybo.models import Question,Catogory
from django.db.models import Q
# Create your views here.
# def index(request,category_id=1):
#     # category = get_object_or_404(Catogory,pk=category_id)
#     category_one = get_object_or_404(Catogory,pk=category_id)
#     category_two = get_object_or_404(Catogory,pk=2)
#     # category_list = Catogory.objects.all()
#     question_list_one = Question.objects.filter(category=category_one.id).order_by('-create_date')[:5]    
#     question_list_two = Question.objects.filter(category=category_two.id).order_by('-create_date')[:5]    
#     # question_list = Question.objects.all()
#     # question_list = question_list.filter(
#     #             Q(category_icontains=1) 
#     #     )
#     # print(question_list)
#     # return HttpResponse(question_list_two)
#     context = {"question_list_one":question_list_one,"question_list_two":question_list_two}
#     return render(request,'main/main.html',context)

def index(request):
  return HttpResponse('안녕하세요')