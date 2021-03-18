from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import *

# admin.site.register(Customer)
# admin.site.register(Category)
# admin.site.register(MetaProduct)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
# admin.site.register(ProductOpinion)
# admin.site.register(FavouriteProduct)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MetaProduct)
class MetaProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'availability', 'digital', 'description', 'image')
    list_filter = ('category', 'availability', 'digital')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('meta_product', 'measure', 'package', 'price', 'availability')
    list_filter = ('meta_product', 'measure', 'package', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'complete',
                    'date_ordered',
                    'show_shipping_address', 'show_if_shipping_is_required',
                    'get_cart_total', 'get_cart_items', 'view_products_link', 'get_orderitems')
    list_filter = ('complete', 'date_ordered')
    # how to filter by 'show_if_shipping_is_required'?

    def view_products_link(self, obj):
        count = obj.orderitem_set.count()
        url = (
            reverse('admin:store_orderitem_changelist')
            + "?"
            + urlencode({'order__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, count)

    view_products_link.short_description = 'Number of product types'

    def show_shipping_address(self, obj):
        result = ShippingAddress.objects.get(id=obj.id)
        return result

    show_shipping_address.short_description = 'Shipping Address'

    def show_if_shipping_is_required(self, obj):
        result = False
        orderitems = obj.orderitem_set.all()
        for i in orderitems:
            if i.product.digital is False:
                result = True
        return result

    show_if_shipping_is_required.short_description = 'Shipping Required'


@admin.register(OrderComment)
class OrderCommentAdmin(admin.ModelAdmin):
    list_display = ('order', 'comment')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'get_total', 'date_added')
    list_filter = ('product', 'date_added')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'address',
                    'city', 'state', 'zipcode', 'date_added')
    list_filter = ('customer',)


@admin.register(ProductOpinion)
class ProductOpinionAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating',
                    'title', 'opinion', 'date_created')
    list_filter = ('product', 'customer', 'rating', 'date_created')
    search_fields = ('title__startswith', 'opinion__startswith', )


@admin.register(FavouriteProduct)
class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ('meta_product', 'customer', 'favourite')
    list_filter = ('meta_product', 'customer')

