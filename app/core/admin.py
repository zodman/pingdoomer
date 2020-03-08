from django.contrib import admin
from .models import Account, Host


class AdminHost(admin.ModelAdmin):
    list_display = ("id","account", "hostname", "type")
    list_select_related  = ("account", )

admin.site.register(Account)
admin.site.register(Host, AdminHost)
