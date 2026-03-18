from django import forms
from f_board.models import F_board



class FForm(forms.ModelForm):
    class Meta:
        model = F_board
        
        fields = ['f_title','f_contents', 'f_file_one', 'f_file_two', 'f_file_three']        

        labels = {
            'f_title': '제목',
            'f_contents': '내용',            
            'f_file_one': '파일1',
            'f_file_two': '파일2',
            'f_file_three': '파일3',
        }  

        