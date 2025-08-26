from django.db import models
# from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

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
    b_subject= models.TextField()
    b_content = models.TextField()
        
    b_link_one = models.TextField(null=True, blank=True)
    b_link_two = models.TextField(null=True, blank=True)
    b_file_one = models.FileField(upload_to="files/", null=True, blank=True)
    b_file_two = models.FileField(upload_to="files/", null=True, blank=True)
    b_file_three= models.FileField(upload_to="files/", null=True, blank=True)
    b_status = models.IntegerField()
    b_cnt = models.IntegerField()    
    def __str__(self):
        return self.subject