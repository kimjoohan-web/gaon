from django.contrib import admin

# Register your models here.
from .models import company_info
from .models import subject_db


class company_infoAdmin(admin.ModelAdmin):
    list_display =['c_name','c_yn','c_number','c_date']

class subject_dbAdmin(admin.ModelAdmin):
    list_display =['s_title','c_idx','s_gubun','start_date','end_date','sum_total','su_total','etc_total','s_date']

admin.site.register(company_info,company_infoAdmin)
admin.site.register(subject_db,subject_dbAdmin) 