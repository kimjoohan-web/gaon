from django import forms
from board.models import Q_board
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class QForm(forms.ModelForm):
    class Meta:
        model = Q_board
        fields = ['b_subject','b_content','b_err_gubun']
        # widgets = {
        #     # 'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     # 'b_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        #     #'b_content': forms.Textarea,
            
        # }
        widgets = {
                'b_content': SummernoteWidget(),
            }
        labels = {
            'b_subject': '제목',
            'b_content': '내용',
            'b_err_gubun':'장애구분'
        }  

        
