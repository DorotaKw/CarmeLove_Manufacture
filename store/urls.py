from django.urls import path

from .views import *

app_name = 'store'

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
    path('<int:meta_product_id>/meta_product/', meta_product, name="meta_product"),
    path('favourites/', favourites, name='favourites'),
  
]

