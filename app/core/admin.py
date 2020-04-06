from django.contrib import admin
from .models import Account, Host, Alert

class AdminHost(admin.ModelAdmin):
    list_display = ("id", "account", "hostname", "type")
    list_select_related = ("account", )


class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "host", "account")

admin.site.register(Account)
admin.site.register(Host, AdminHost)
admin.site.register(Alert, AlertAdmin)
