from django.contrib import admin

from .models import Gdraft_db, Gdraft_log, Gdraft_status

# Register your models here.
admin.site.register(Gdraft_db)
admin.site.register(Gdraft_log)
admin.site.register(Gdraft_status)