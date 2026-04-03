from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Waitboard(models.Model):
    w_id = models.AutoField(primary_key=True)
    w_name = models.CharField(max_length=100)
    w_hp = models.CharField(max_length=20)
    w_created_at = models.DateTimeField(auto_now_add=True)
    w_YN = models.CharField(max_length=1, default='N')
    def __str__(self):
        return self.w_name
   
    



    

