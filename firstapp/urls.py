from django.urls import path
from . import views

urlpatterns = [path("check/", views.aview), path("", views.aview)]
