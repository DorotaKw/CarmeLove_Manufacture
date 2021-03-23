from django.urls import path

from .views import *

app_name = 'about_cl'

urlpatterns = [
    path('', about_us, name="about_us"),
]