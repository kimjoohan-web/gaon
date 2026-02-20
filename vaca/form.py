
from common import forms
from django import forms
from .models import LeaveRequest, LeaveType
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class vacaform(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        labels = {
            'leave_type': '휴가 유형',
            'start_date': '시작 날짜',
            'end_date': '종료 날짜',
            'reason': '사유'                           
        }
        widgets = {
            'reason': SummernoteWidget(),
        }   

