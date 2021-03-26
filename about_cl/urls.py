from django.urls import path

from .views import *

app_name = 'about_cl'

urlpatterns = [
    path('<slug:slug>/', AboutCarmeLoveView.as_view(), name='about_carmelove'),
]
