
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from pybo.models import Question,Catogory
from django.db.models import Q
# Create your views here.
def index(request):
    
    # return HttpResponse("안녕하세요")
    # context = {"question_list_one":question_list_one,"question_list_two":question_list_two}    
    context={}
    return render(request,'gaonsample/index.html',context)