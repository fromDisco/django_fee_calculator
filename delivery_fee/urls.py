# import django modules/libraries
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# import app modules
from . import views

urlpatterns = [path("", csrf_exempt(views.CalculateFee.as_view()), name="calculate")]
