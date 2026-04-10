import json
from unittest import result
from urllib import request
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from waitboard.forms import  WaitForm


from .models import Waitboard
from django.core.paginator import Paginator
# Create your views here.

# @receiver(post_save, sender=Waitboard)
# def waitboard_post_save(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "wait_list",
#         {
#             "type": "wait_list_message",
#             "waiters": list(Waitboard.objects.values())
#         }
#     )

def wait(request):
    wait_list = Waitboard.objects.all().order_by('-w_created_at')
    pagenator = Paginator(wait_list, 10)  # 페이지당 10개씩 보여주기
    page = request.GET.get('page', 1)  # 페이지 번호 가져오기, 기본값은 1
    wait_list = pagenator.get_page(page)  # 해당 페이지의 객체 가져오기

    return render(request, 'waitboard/wait.html', {'wait_list': wait_list})


def wait_create(request):
    if request.method == 'POST':
        w_name = request.POST['w_name']
        w_hp = request.POST['w_hp']
        #전화번호가 있는지 없는지 유무 확인
        wait = Waitboard.objects.filter(w_hp=w_hp).first()
        if wait:
            error_message = '이미 등록된 전화번호입니다.'
            context = {
                'form': WaitForm(),
                'error_message': error_message,
            }
            return render(request, 'waitboard/wait_form.html', context)
        
        Waitboard.objects.create(w_name=w_name, w_hp=w_hp)
        return redirect('waitboard:wait')
    else:
        context = {
            'form': WaitForm(),
        }
        return render(request, 'waitboard/wait_form.html', context)
    
def wait_detail(request, w_id):
    wait = Waitboard.objects.get(w_id=w_id)
    context = {
        'wait': wait,
    }
    return render(request, 'waitboard/wait_detail.html', context) 


def wait_modify(request, w_id):
    wait = Waitboard.objects.get(w_id=w_id)
    if request.method == 'POST':
        w_name = request.POST['w_name']
        w_hp = request.POST['w_hp']
        wait.w_name = w_name
        wait.w_hp = w_hp
        wait.save()
        return redirect('waitboard:wait_detail', w_id=wait.w_id)
    else:
        context = {
            'form': WaitForm(instance=wait),
            'wait': wait,
        }
        return render(request, 'waitboard/wait_form.html', context) 
    
def wait_delete(request, w_id):
    wait = Waitboard.objects.get(w_id=w_id)
    wait.delete()
    return redirect('waitboard:wait')   

def wait_list(request):
    wait_list = Waitboard.objects.all().order_by('-w_created_at')
    context = {
        'wait_list': wait_list,
    }
    return render(request, 'waitboard/wait_list.html', context)


def waiting(request):

    return render(request, 'waitboard/waiting_dashboard.html')