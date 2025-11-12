from django.contrib import admin

# Register your models here.



from .models import Q_board
from .models import Category
from .models import Jik_gread
from .models import Approve

# class QuestionAdmin(admin.ModelAdmin):
#     search_fields =['subject']


admin.site.register(Q_board)
admin.site.register(Category)
admin.site.register(Jik_gread)
admin.site.register(Approve)  