from django.db import models
from django.contrib.auth.models import User
# Create your models here.  dddd

class Catogory(models.Model):
    name = models.TextField(max_length=50,unique=True)
    def __str__(self):
        return self.name

class Question(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_question')    
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    voter = models.ManyToManyField(User,related_name='voter_question')
    category = models.ForeignKey(Catogory,on_delete=models.CASCADE)
    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    voter = models.ManyToManyField(User,related_name='voter_answer')

class Qcomment(models.Model):
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    question =models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True)    
    content = models.TextField()
    create_date = models.DateTimeField(null=True,blank=True)

class Acomment(models.Model):
    author =models.ForeignKey(User,on_delete=models.CASCADE)    
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null= True,blank=True)
    content = models.TextField()
    create_date = models.DateTimeField(null=True,blank=True)


        