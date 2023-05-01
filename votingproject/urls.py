
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #Admin base url
    path("admin/", admin.site.urls, name='admin_base_url'),

    # base url and API
    path('', include("voting.urls"), name='base_url'),
    path("api/", include("voting.urls")),

    # ussd url
    path("ussd/", include("ussd.urls")),

    # rest_framework urls
    path("api/", include("rest_framework.urls")),
]
