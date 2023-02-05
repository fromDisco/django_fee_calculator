# import django modules/libraries
from django.urls import path

# import app modules
from . import views

urlpatterns = [
    path("", views.calculate_fee)
]
