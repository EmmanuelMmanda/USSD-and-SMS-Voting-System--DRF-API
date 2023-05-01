from django.urls import include, path
from .views import USSDView


urlpatterns = [
    path ("", USSDView.as_view(), name="ussd"),
]
