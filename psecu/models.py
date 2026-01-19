from django.db import models
from django.contrib.auth.models import User 
from board.models import Jik_gread   
# Create your models here.
class pc_secu_title_db(models.Model):
    p_m_idx = models.AutoField(primary_key=True)
    p_m_b=models.IntegerField()
    p_m_m=models.IntegerField()
    p_m_s=models.IntegerField()
    p_m_title=models.CharField(max_length=400)
    p_m_indate=models.DateTimeField()
    p_m_YN=models.CharField(max_length=1)
    p_m_asc=models.IntegerField()
    def __str__(self):
        return self.p_m_title   
    
class pc_secu_ck_db(models.Model):
    p_m_c_idx = models.AutoField(primary_key=True)
    p_m_idx=models.ForeignKey(pc_secu_title_db, on_delete=models.CASCADE)
    p_m_c_val=models.CharField(max_length=500)    
    p_m_c_id=models.ForeignKey(User,on_delete=models.CASCADE)
    p_m_c_indate=models.DateTimeField()
    p_m_c_wdate=models.DateTimeField(null=True, blank=True)
    p_m_b=models.IntegerField()
    p_wb_idx=models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.p_m_c_val       
    
class pc_secu_cf_db(models.Model):
    p_m_cf_idx = models.AutoField(primary_key=True)
    p_m_idx=models.ForeignKey(pc_secu_title_db, on_delete=models.CASCADE)
    p_m_cf_val=models.IntegerField()        
    p_m_c_id=models.ForeignKey(User,on_delete=models.CASCADE)
    p_m_jik_id= models.ForeignKey('board.Jik_gread',on_delete=models.CASCADE)
    p_m_cf_indate=models.DateTimeField()
    p_m_cf_wdate=models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.p_m_cf_val
    

class pc_work_board_db(models.Model):
    p_wb_idx = models.AutoField(primary_key=True)
    p_wb_b=models.IntegerField()    
    p_wb_id=models.ForeignKey(User,on_delete=models.CASCADE)
    p_wb_indate=models.DateTimeField()
    p_wb_wdate=models.DateTimeField(null=True, blank=True)
    p_wb_check=models.CharField(max_length=1)
    p_wb_review_check=models.CharField(max_length=1)
    p_wb_check_userID=models.IntegerField(null=True, blank=True)
    p_wb_review_check_userID=models.IntegerField(null=True, blank=True)    
    def __str__(self):
        return str(self.p_wb_idx)