from django.db import models
# from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User 



class F_board(models.Model):    
    f_id = models.AutoField(primary_key=True)
    f_name = models.ForeignKey(User,on_delete=models.CASCADE ,related_name='f_name')
    f_create_date = models.DateTimeField()    
    f_title= models.CharField(max_length=200)
    f_contents = models.TextField()        
    f_file_one = models.FileField(upload_to="f_files/", null=True, blank=True)
    f_file_two = models.FileField(upload_to="f_files/", null=True, blank=True)
    f_file_three= models.FileField(upload_to="f_files/", null=True, blank=True)    
    f_cnt = models.IntegerField()    
    f_d_cnt = models.IntegerField()
    f_yn = models.CharField(max_length=1)
    def __str__(self):
        return self.f_title
    