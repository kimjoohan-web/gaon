from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect,resolve_url
from django.utils import timezone
from django.core.paginator import Paginator



from pybo.forms import AnswerForm,AnswerCommentForm
from pybo.models import Question, Answer

# Create your views here.
# from django.http import HttpResponse


@login_required(login_url='common:login')
def answer_create(request,category_id,question_id):
    question =get_object_or_404(Question,pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            
            answer.save()
            # return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#answer_{}'.format(resolve_url('manager:detail',category_id=category_id,question_id= answer.question.id),answer.id))
    else:
        # return HttpResponseNotAllowed('Only POST is possible.')
        form =AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'manager/mpybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request,category_id, answer_id):
    answer =get_object_or_404(Answer,pk=answer_id)    
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('manager:detail',category_id=category_id, question_id=answer.question.id)
        
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            # return redirect('manager:detail', question_id=answer.question.id)            
            return redirect('{}#answer_{}'.format(resolve_url('manager:detail',category_id=category_id, question_id=answer.question.id), answer.id))
    else :
            form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'manager/mpybo/answer_form.html', context)
@login_required(login_url='common:login')
def answer_delete(request,category_id,answer_id):
    answer = get_object_or_404(Answer,pk=answer_id)

    if request.user != answer.author :
        messages.error(request,'삭제권한이 없습니다.')
    
    else:
        answer.delete()
        
    return redirect('manager:detail',category_id=category_id,question_id = answer.question.id)
    


@login_required(login_url='common:login')
def answer_vote(request,category_id,answer_id):
    answer = get_object_or_404(Answer,pk=answer_id)
    if request.user == answer.author :
        messages.error(request,"본인이 작성한 답변은 추천을 할 수가 없습니다.")
    else :
        answer.voter.add(request.user)

    # return redirect ('manager:detail',question_id = answer.question.id)
    return redirect('{}#answer_{}'.format(resolve_url('manager:detail',category_id=category_id,question_id= answer.question.id),answer.id))



@login_required(login_url='common:login')
def answer_comment(request,category_id,answer_id):
     answer = get_object_or_404(Answer,pk = answer_id)
     
     form = AnswerCommentForm(request.POST)
     if request.method == "POST":
        if form.is_valid():
            acomment = form.save(commit=False)
            acomment.author = request.user
            acomment.answer = answer             
            acomment.create_date = timezone.now()                    
            acomment.save()
            # return redirect('pybo:detail', answer_id=answer.id)
        return redirect('{}#answer_{}'.format(resolve_url('manager:detail',category_id=category_id,question_id= answer.question.id),answer.id))
