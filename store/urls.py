from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('store/', store, name="store"),
    path('<int:category_id>/category/', category, name="category"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', update_item, name="update_item"),
    path('process_order/', process_order, name="process_order"),
    path('<int:meta_product_id>/meta_product/', meta_product, name="meta_product"),
    path('orders_history/', orders_history, name="orders_history"),
    path('<int:user_order_id>/order_history/', order_history, name="order_history"),
    # path('<int:product_id>/product/', product, name="product"),
]

