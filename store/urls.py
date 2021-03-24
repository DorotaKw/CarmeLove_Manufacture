from django.urls import path

from .views import *

app_name = 'store'

urlpatterns = [
    # path('', home, name="home"),
    path('', home, name="home"),
    path('store/', StoreView.as_view(), name="store"),
    path('store/<slug:slug>', meta_product, name="meta_product"),
    path('store/categories/', CategoriesView.as_view(), name="categories"),
    path('store/categories/<slug:slug>', CategoryView.as_view(), name="category"),

    # paths after add items to cart
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', update_item, name="update_item"),
    path('process_order/', process_order, name="process_order"),
]

