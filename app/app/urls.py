from django.contrib import admin
from django.urls import path, include
from core.views import AccountViewset, HostViewset
from django.shortcuts import redirect

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewset)

hosts_router = routers.NestedDefaultRouter(router, r'accounts', lookup='accounts')
hosts_router.register(r"hosts", HostViewset, basename="account-hosts")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(hosts_router.urls)),
]
