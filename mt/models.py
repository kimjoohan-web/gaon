from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class company_info(models.Model):    
    c_idx = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=200)
    c_yn = models.CharField(max_length=1)
    c_number = models.CharField(max_length=50,null=True,blank=True)
    c_date = models.DateField()   

    def __str__(self):
        return self.c_name
    
class subject_db(models.Model):
    s_idx = models.AutoField(primary_key=True)
    c_idx= models.ForeignKey(company_info,on_delete=models.CASCADE)    
    s_gubun = models.CharField(max_length=1)
    s_title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    sum_total = models.IntegerField()
    su_total=models.IntegerField()
    etc_total=models.IntegerField()
    s_date = models.DateField()   

    def __str__(self):
        return self.s_title 
    


