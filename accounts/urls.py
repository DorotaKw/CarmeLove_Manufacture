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

    # for Customer
    path('orders_history/', orders_history, name="orders_history"),
    path('orders_history/<int:user_order_id>/order_history/', order_history, name="order_history"),

    # for Admin
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:order_details_id>/order_details/', order_details, name='order_details'),
    path('orders/orders_completed/', OrdersCompletedView.as_view(), name='orders_completed'),
    path('orders/orders_completed/<int:completed_order_details_id>/completed_order_details/',
         completed_order_details, name='completed_order_details'),
]
