from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', SubmittablePasswordChangeView.as_view(),
         name='password_change'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
