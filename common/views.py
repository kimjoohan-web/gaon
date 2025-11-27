from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from common.forms import UserForm,Userpassword,UserPasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
import string
import random
from django.contrib import messages
from django.contrib.auth.hashers import check_password


def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            # return redirect('categoryView')
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def forgot_password(request):
    
    if request.method == "POST":

        string.ascii_letters
        string.digits
        alphanumeric = string.ascii_letters + string.digits
        list(set(alphanumeric) - set('lIO0'))

        pw = str()
        chars = list(set(alphanumeric) - set('lIO0')) + ['_']
        for i in range(16):
            pw += random.choice(chars)


        return HttpResponse(f"{pw} 입니다..") 
    


        # form = Userpassword(request.POST) 
        # if form.is_valid():
        #     femail = form.cleaned_data['femail']
        #     user =get_object_or_404(User,email=femail)
        #     new_password = '1111'
        #     user.set_password(new_password)
        #     user.save()
        #     return redirect('categoryView')
            # return HttpResponse(f"{femail} 입니다..")    
    else:
        form = Userpassword(request.POST)
        return render(request, 'common/forgot_password.html', {'form': form})


    # if request.method == "POST":
    #     form = Userpassword(request.POST)        
    #     femail =request.femail
    #     user =get_object_or_404(User,email=femail)        
        
       
    #     if form.is_valid():
    #         new_password = '1111'
    #         user.set_password(new_password)
    #         user.save()
    #         return redirect('categoryView')
    # else:
    #     form = Userpassword()   
    #     return render(request, 'common/forgot_password.html', {'form': form})


def pwd_email(request,femail):
    # 먼저 암호 생성
    # 패스워드 업데이트
    # 이메일 전송
    # imsipwd = '1111'
    pass


def pwd_change(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user

            var = check_password(request.POST['old_pwd'],user.password)
            # return HttpResponse(f"기존 패스워드 {user.password} ,입력받은 패스워드 {request.POST['old_pwd']} ,{var} 입니다..") 
            if var :# 기존 비밀번호와 입력받은 비번이 같을경우 
                userpwd = request.POST['new_pwd']
                userpwdcf = request.POST['new_pwd_confirm']

                if userpwd == userpwdcf : # 입력받은 비번과 비번확인이 같다면 진행
                    user.set_password(userpwd)
                    user.save()
                    messages.success(request,'비번이 변경완료 되었습니다.')
                    login(request, user)  # 로그인
                    return redirect ('categoryView')
                    
                else :
                    messages.error(request, '입력받은 비번과 비번확인이 다릅니다.')
                    return render(request, 'common/pwd_change.html', {'form': form})
        
            else :
                messages.error(request, '기존의 비번이 다릅니다.')
                return render(request, 'common/pwd_change.html', {'form': form})



       
    else:
        form = UserPasswordChangeForm(request.POST)
        return render(request, 'common/pwd_change.html', {'form': form})