from django.db import models

# Create your models here.
class LeaveType(models.Model):
    leave_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    deduct_from_balance = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True)    

    def __str__(self):
        return self.type_name
    
class LeaveBalance(models.Model):
    balance_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    year = models.IntegerField()
    total_days = models.FloatField()
    used_days = models.FloatField(default=0)
    remaining_days = models.FloatField(default=0)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.username} - {self.leave_type.type_name} ({self.year})"
    

class LeaveRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Approved, Rejected
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Leave Request {self.request_id} by {self.user_id.username} for {self.leave_type.type_name}"
    

class LeaveApproval(models.Model):
    approval_id = models.AutoField(primary_key=True)
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    approver_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='approver')
    approver_order = models.IntegerField()  # 1 for first approver, 2 for second approver, etc.    
    approval_status = models.CharField(max_length=20,default='Pending')  # Approved, Rejected    
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval {self.approval_id} for Request {self.leave_request.request_id} by {self.approver_id.username}"


