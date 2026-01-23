from django.db import models
from django.contrib.auth.models import User 
from board.models import Jik_gread   
# Create your models here.

class Gdraft_db(models.Model):
    dr_idx = models.AutoField(primary_key=True)
    dr_no = models.CharField(max_length=20, unique=True)
    dr_date = models.DateField(blank=True, null=True)
    dr_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dr_title = models.CharField(max_length=200)       
    dr_content = models.TextField()
    dr_attachfile = models.FileField(upload_to='gdraft/%Y/%m/%d/', blank=True, null=True)
    dr_indate = models.DateField(blank=True, null=True)
    dr_save_status = models.CharField(max_length=10, choices=(('임시저장','임시저장'),('작성완료','작성완료')), default='임시저장')
    dr_status = models.CharField(max_length=10, choices=(('결재대기','결재대기'),('결재완료','결재완료'),('반려','반려')), default='결재대기')    

    def __str__(self):
        return self.dr_title
    



class Gdraft_status(models.Model):
    drs_idx = models.AutoField(primary_key=True)
    dr_idx = models.ForeignKey(Gdraft_db, on_delete=models.CASCADE)
    drs_status = models.CharField(max_length=10, choices=(('대기','대기'),('승인','승인'),('반려','반려')), default='대기')
    drs_jik = models.IntegerField()  # 직급 ID
    drs_id= models.ForeignKey(User, on_delete=models.CASCADE, related_name='drafter')
    drs_date = models.DateField(blank=True, null=True)
    drs_comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.dr_idx.dr_no} - {self.drs_jik.jik_name} - {self.drs_status}"
    
class Gdraft_log(models.Model):
    drl_idx = models.AutoField(primary_key=True)
    dr_idx = models.ForeignKey(Gdraft_db, on_delete=models.CASCADE)
    drl_action = models.CharField(max_length=50)
    drl_id = models.ForeignKey(User, on_delete=models.CASCADE)
    drl_date = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f"{self.dr_idx.dr_no} - {self.drl_action} - {self.drl_id.username}"
    

