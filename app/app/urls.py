from django.contrib import admin
from django.urls import path, include
from core.views import AccountViewset, HostViewset,AlertViewset
from django.shortcuts import redirect

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewset)

hosts_router = routers.NestedDefaultRouter(router, r'accounts',
                                           lookup='accounts')
hosts_router.register(r"hosts", HostViewset, basename="account-hosts")

alerts_router = routers.NestedDefaultRouter(hosts_router, r'hosts',
                                            lookup='hosts')
alerts_router.register("alerts", AlertViewset, basename="alerts")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(hosts_router.urls)),
    path("api/", include(alerts_router.urls)),
]
