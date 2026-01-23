from django import forms
from .models import Gdraft_db
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
class gdrform(forms.ModelForm):
    class Meta:
        model = Gdraft_db
        fields = ['dr_no', 'dr_title', 'dr_content', 'dr_save_status','dr_date']
        labels = {
            'dr_no': '문서번호',
            'dr_title': '제목',
            'dr_content': '내용',               
            'dr_save_status': '저장상태',     
            'dr_date': '기안날짜',      
        }
        widgets = {
            'dr_content': SummernoteWidget(),
        }   


class selectform(forms.ModelForm):
   CHOICES = [('결재대기','결재대기'),('결재완료','결재완료'),('반려','반려')]
   dr_status = forms.ChoiceField(choices=CHOICES, label='결재상태', widget=forms.Select(attrs={'class':'form-select'}))
   class Meta:
        model = Gdraft_db
        fields = ['dr_status']  