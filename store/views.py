import datetime

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView

from .models import Customer, Category, Product, Order, OrderItem, ProductOpinion, MetaProduct
from .forms import ProductOpinionForm


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']
    categories = Category.objects.all()
    meta_products = MetaProduct.objects.all()
    # products = Product.objects.all()
    context = {'categories': categories, 'meta_products': meta_products, 'cart_items': cart_items}   #'products': products,
    return render(request, 'store.html', context)


def category(request, category_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']
    categories = Category.objects.all()
    viewed_category = Category.objects.get(id=category_id)
    meta_products = MetaProduct.objects.filter(category=category_id).order_by('name').all()
    context = {'categories': categories, 'viewed_category': viewed_category,
               'meta_products': meta_products, 'cart_items': cart_items}
    return render(request, 'category.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'checkout.html', context)


def update_item(request):
    return JsonResponse('Product was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        print('User is not logged in...')
    return JsonResponse('Payment submitted...', safe=False)


def meta_product(request, meta_product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        form = ProductOpinionForm()
        viewed_meta_product = MetaProduct.objects.get(id=meta_product_id)
        products = viewed_meta_product.product_set.all()
        opinions = ProductOpinion.objects.filter(product=viewed_meta_product)
        if request.method == 'POST':
            form = ProductOpinionForm(request.POST)
            if form.is_valid():
                new_opinion = form.save(commit=False)
                new_opinion.customer = request.user.customer
                new_opinion.product = viewed_meta_product
                new_opinion.save()
                user_new_opinion = new_opinion
                context = {'meta_product': viewed_meta_product,
                           'products': products,
                           'form': form,
                           'user_new_opinion': user_new_opinion,
                           'opinions': opinions,
                           'cart_items': cart_items}
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']
        # for now it's the only idea I have, it's working, but view is too fat.
        # maybe JS or/and CSS will help?
        form = None

    viewed_meta_product = MetaProduct.objects.get(id=meta_product_id)
    products = viewed_meta_product.product_set.all()
    opinions = ProductOpinion.objects.filter(product=viewed_meta_product)
    context = {'meta_product': viewed_meta_product,
               'products': products,
               'form': form,
               'opinions': opinions,
               'cart_items': cart_items}
    return render(request, 'meta_product.html', context)


# def product(request, product_id):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cart_items = order.get_cart_items
#         form = ProductOpinionForm()
#         viewed_product = Product.objects.get(id=product_id)
#         opinions = ProductOpinion.objects.filter(product=viewed_product)
#         if request.method == 'POST':
#             form = ProductOpinionForm(request.POST)
#             if form.is_valid():
#                 new_opinion = form.save(commit=False)
#                 new_opinion.customer = request.user.customer
#                 new_opinion.product = viewed_product
#                 new_opinion.save()
#                 user_new_opinion = new_opinion
#                 context = {'product': viewed_product,
#                            'form': form,
#                            'user_new_opinion': user_new_opinion,
#                            'opinions': opinions,
#                            'cart_items': cart_items}
#                 return render(request, 'product.html', context)
#     else:
#         items = []
#         order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#         cart_items = order['get_cart_items']
#         # for now it's the only idea I have, it's working, but view is too fat.
#         # maybe JS or/and CSS will help?
#         form = None
#
#     viewed_product = Product.objects.get(id=product_id)
#     opinions = ProductOpinion.objects.filter(product=viewed_product)
#     context = {'product': viewed_product, 'form': form, 'opinions': opinions, 'cart_items': cart_items}
#     return render(request, 'product.html', context)

def order_history(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # items = order.orderitem_set.all()
        # cart_items = order.get_cart_items
        user_orders = Order.objects.filter(customer=customer, complete=True)
        for user_order in user_orders:
            history_items = user_order.get_orderitems

        #completed = user_orders.objects.filter(complete=True)
        #user_orders = user_all_orders.objects.filter(complete=True).all()
        # user_order = [print(user_order) for user_order in user_orders]
        #history_items = user_orders.orderitems_set.all()

        # for user_order in user_orders:
        #     if user_order.complete is True:
        #         history_items = user_order.orderitem_set.all()
        #for item in history_items:

        context = {'user_orders': user_orders,
                   'history_items': history_items}
        return render(request, 'order_history.html', context)

        # context = {'items': items,
        #            'user_orders': user_orders,
        #            'history_items': history_items,
        #            'cart_items': cart_items}
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    #     cart_items = order['get_cart_items']
    #     user_orders = None
    #     history_items = None
    # history_items = [user_order.orderitem_set.all() for user_order in user_orders]

               # 'items': items, 'order': order, 'cart_items': cart_items}
    # context = {'user_orders': user_orders, 'history_items': history_items}
    # return render(request, 'order_history.html', context)

