from django.contrib import admin

# Register your models here.



from .models import Q_board
from .models import Category

# class QuestionAdmin(admin.ModelAdmin):
#     search_fields =['subject']


admin.site.register(Q_board)
admin.site.register(Category)