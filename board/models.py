from django.db import models
# from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField

# Create your models here.

class Category(models.Model):
    name = models.TextField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    

class Q_board(models.Model):
    
    b_gubun =models.ForeignKey(Category,on_delete=models.CASCADE)    
    b_name = models.ForeignKey(User,on_delete=models.CASCADE)
    b_create_date = models.DateTimeField()
    b_err_gubun=models.IntegerField()
    b_subject= models.CharField()
    b_content = models.TextField()
    # b_content = SummernoteTextField()
    b_link_one = models.CharField(null=True, blank=True)
    b_link_two = models.CharField(null=True, blank=True)
    b_file_one = models.FileField(upload_to="files/", null=True, blank=True)
    b_file_two = models.FileField(upload_to="files/", null=True, blank=True)
    b_file_three= models.FileField(upload_to="files/", null=True, blank=True)
    b_status = models.IntegerField()
    b_cnt = models.IntegerField()    
    def __str__(self):
        return self.b_subject
    


class Jik_gread(models.Model):
    j_id = models.ForeignKey(User,on_delete=models.CASCADE)
    j_gread = models.IntegerField()
    j_name = models.CharField(max_length=50)
    j_yn = models.CharField(max_length=1)
   
    

class Approve(models.Model):
    a_board = models.ForeignKey(Q_board,on_delete=models.CASCADE)    
    a_jik = models.ForeignKey(Jik_gread,on_delete=models.CASCADE)
    a_approve = models.CharField(max_length=1)    
    a_approve_date = models.DateTimeField(null=True, blank=True)    
    