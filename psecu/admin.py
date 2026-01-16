from django.contrib import admin
from .models import pc_secu_title_db, pc_work_board_db
from .models import pc_secu_ck_db
from .models import pc_secu_cf_db
# Register your models here.
admin.site.register(pc_secu_title_db)
admin.site.register(pc_secu_ck_db)
admin.site.register(pc_secu_cf_db)
admin.site.register(pc_work_board_db)