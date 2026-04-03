from django import forms
from waitboard.models import  Waitboard   



class WaitForm(forms.ModelForm):
    class Meta:
        model = Waitboard
        
        fields = ['w_name','w_hp']        

        labels = {
            'w_name': '이름',
            'w_hp': '전화번호',       
        }  

        