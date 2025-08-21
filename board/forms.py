from django import forms
from board.models import Q_board

class QForm(forms.ModelForm):
    class Meta:
        model = Q_board
        fields = ['b_subject','b_content','b_err_gubun']
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            
        # }
        labels = {
            'b_subject': '제목',
            'b_content': '내용',
            'b_err_gubun':'장애구분'
        }  
