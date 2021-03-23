import datetime


from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView

import json

from .models import Customer, Category, Product, Order, OrderItem,\
    ProductOpinion, MetaProduct
from .forms import ProductOpinionForm, OrderCommentForm

from .utils import *

from about_cl.models import Article


def set_initial_cart_status(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']
    context = {'cart_items': cart_items}
    return context


def home(request):
    data = cart_data(request)

    cart_items = data['cart_items']

    categories = Category.objects.all()
    articles = Article.objects.all()
    context = {'categories': categories,
               'cart_items': cart_items,
               'articles': articles}
    return render(request, 'home.html', context)


class StoreView(ListView):
    template_name = 'store.html'
    context_object_name = 'meta_products'
    model = MetaProduct

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = set_initial_cart_status(request=self.request)
        cart_items = cart_item.get('cart_items')
        context.update({
            'categories': Category.objects.all(),
            'cart_items': cart_items,
        })
        return context

    def get_queryset(self):
        return MetaProduct.objects.all().order_by('name')


class CategoriesView(ListView):
    template_name = 'categories.html'
    context_object_name = 'categories'
    model = Category

    def get_queryset(self):
        return Category.objects.order_by('name')


class CategoryView(ListView):
    template_name = 'category.html'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = set_initial_cart_status(request=self.request)
        cart_items = cart_item.get('cart_items')
        categories = Category.objects.all()
        viewed_category = get_object_or_404(Category, id=self.kwargs['category_id'])
        meta_products = MetaProduct.objects.filter(category=self.kwargs['category_id']).order_by('name').all()
        context = {'categories': categories,
                   'viewed_category': viewed_category,
                   'meta_products': meta_products,
                   'cart_items': cart_items}
        return context


def cart(request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()

    context = {'categories': categories, 'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'cart.html', context)


def checkout(request):
    form = OrderCommentForm()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        try:
            comment = OrderComment.objects.get(order=order)
            if comment:
                if request.method == 'POST':
                    comment.delete()
                    form = OrderCommentForm(request.POST)
                    if form.is_valid():
                        order_comment = form.save(commit=False)
                        # without this line, there are created new empty orders with comment
                        # but without it, comment is still on the page
                        order_comment.order = order
                        # maybe save comment while make a transfer?
                        order_comment.save()
                        context = {}
                        context['order_comment'] = order_comment
                        context['customer'] = customer
                        context['form'] = form
        except OrderComment.DoesNotExist:
            if request.method == 'POST':
                form = OrderCommentForm(request.POST)
                if form.is_valid():
                    order_comment = form.save(commit=False)
                    order_comment.order = order
                    order_comment.save()
                    context = {}
                    context['order_comment'] = order_comment
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']

    # past code below:
    # earlier when user is not logged in:
    # Exception Value:
    # Field 'id' expected a number but got {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}.

    # data = cart_data(request)
    # customer = data['customer']
    # cart_items = data['cart_items']
    # order = data['order']
    # items = data['items']

    categories = Category.objects.all()
    context = {'categories': categories,
               'items': items, 'order': order,
               'cart_items': cart_items, 'form': form}
    return render(request, 'checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']   # productId
    action = data['action']
    print('Action:', action)
    print('Product:', product_id)   # productId

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Product was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = quest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping is True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted...', safe=False)


def meta_product(request, meta_product_id):
    categories = Category.objects.all()
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
                context = {'categories': categories,
                           'meta_product': viewed_meta_product,
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

    categories = Category.objects.all()
    viewed_meta_product = MetaProduct.objects.get(id=meta_product_id)
    products = viewed_meta_product.product_set.all()
    opinions = ProductOpinion.objects.filter(product=viewed_meta_product)
    context = {'categories': categories,
               'meta_product': viewed_meta_product,
               'products': products,
               'form': form,
               'opinions': opinions,
               'cart_items': cart_items}
    return render(request, 'meta_product.html', context)

