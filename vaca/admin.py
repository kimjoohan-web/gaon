from django.contrib import admin
# Register your models here.
from .models import LeaveType, LeaveBalance, LeaveRequest,LeaveApproval
# Register your models here.
admin.site.register(LeaveType)
admin.site.register(LeaveBalance)
admin.site.register(LeaveRequest)
admin.site.register(LeaveApproval)