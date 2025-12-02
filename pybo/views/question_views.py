from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect,resolve_url
from django.utils import timezone

from ..models import Question,Catogory
from ..forms import QuestionForm
from ..forms import QuestionCommentForm






@login_required(login_url='common:login')
def question_create(request,category_id):
    category =get_object_or_404(Catogory,pk=category_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.category = category
            question.save()
            return redirect('pybo:list',category_id=category.id)
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request,category_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail',category_id=category_id, question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, category_id,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail',category_id=category_id,question_id=question.id)
    question.delete()
    return redirect('pybo:list',category_id=category_id)



@login_required(login_url='common:login')
def question_vote(request, category_id,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
        
    return redirect('pybo:detail',category_id=category_id, question_id=question.id)

@login_required(login_url='common:login')
def question_comment(request, category_id ,question_id):
     question = get_object_or_404(Question,pk = question_id)
     
     form = QuestionCommentForm(request.POST)
     if request.method == "POST":
        if form.is_valid():
            qcomment = form.save(commit=False)
            qcomment.author = request.user
            qcomment.question = question             
            qcomment.create_date = timezone.now()                    
            qcomment.save()
            return redirect('pybo:detail',category_id=category_id, question_id=question.id)
            # return redirect('{}#answer_{}'.format(resolve_url('pybo:detail',question_id= answer.question.id),answer.id))
