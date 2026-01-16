from django import forms
from psecu.models import pc_secu_ck_db

class Pc_secu_ck_Form(forms.ModelForm):
    class Meta:
        model = pc_secu_ck_db
        fields = ['p_m_c_wdate']
        
        labels = {
            'p_m_c_wdate': '작성일',
        }  

