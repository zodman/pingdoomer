from django.contrib import admin
from .models import Account, Host


class AdminHost(admin.ModelAdmin):
    list_display = ("id", "hostname", "type")

admin.site.register(Account)
admin.site.register(Host, AdminHost)
