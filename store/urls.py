from django.urls import path

from .views import *

urlpatterns = [
    # path('', home, name="home"),
    path('', home, name="home"),
    path('store/', StoreView.as_view(), name="store"),
    path('categories/', CategoriesView.as_view(), name="categories"),
    path('categories/<int:category_id>/category/', CategoryView.as_view(), name="category"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', update_item, name="update_item"),
    path('process_order/', process_order, name="process_order"),
    path('<int:meta_product_id>/meta_product/', MetaProductView.as_view(), name="meta_product"),
    path('orders_history/', orders_history, name="orders_history"),
    path('<int:user_order_id>/order_history/', order_history, name="order_history"),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:order_details_id>/order_details/', order_details, name='order_details'),
    path('orders/orders_completed/', OrdersCompletedView.as_view(), name='orders_completed'),
    path('orders/orders_completed/<int:completed_order_details_id>/completed_order_details/', completed_order_details, name='completed_order_details'),
    path('favourites/', favourites, name='favourites'),
  
]

