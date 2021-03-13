import datetime


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
#from django.contrib.admin.views.decorators.staff_member_required import

import json

from .models import Customer, Category, Product, Order, OrderItem,\
    ProductOpinion, MetaProduct, OrderComment, FavouriteProduct
from .forms import ProductOpinionForm, OrderCommentForm

from .utils import *


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


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


class OrdersView(StaffRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'orders.html'
    model = Order
    permission_required = 'store/.orders'


@staff_member_required
def order_details(request, order_details_id):
    viewed_order = Order.objects.get(id=order_details_id)
    order_items = viewed_order.get_orderitems
    context = {'viewed_order': viewed_order, 'order_items': order_items}
    return render(request, 'order_details.html', context)


class OrdersCompletedView(StaffRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'orders_completed.html'
    model = Order
    permission_required = 'store/.orders_completed'

    def get_queryset(self):
        return Order.objects.filter(complete=True)


@staff_member_required
def completed_order_details(request, completed_order_details_id):
    viewed_order_completed = Order.objects.get(id=completed_order_details_id)
    order_items = viewed_order_completed.get_orderitems
    context = {'viewed_order_completed': viewed_order_completed, 'order_items': order_items}
    return render(request, 'completed_order_details.html', context)


def home(request):
    data = cart_data(request)

    cart_items = data['cart_items']

    categories = Category.objects.all()
    about = 'Hi! We are small Manufacture of Sweets!'
    context = {'categories': categories, 'cart_items': cart_items, 'about': about}
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
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
    categories = Category.objects.all()
        
    form = OrderCommentForm()
    if request.method == 'POST':
        form = OrderCommentForm(request.POST)
        if form.is_valid():
            new_order_comment = form.save(commit=False)
            new_order_comment.order = order
            new_order_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    current_order = Order.objects.get(id=order.id)
    order_comment = OrderComment.objects.filter(order=current_order)

    context = {'categories': categories,
               'items': items, 'order': order,
               'cart_items': cart_items,
               'form': form, 'order_comment': order_comment}
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


class MetaProductView(ListView):
    template_name = 'meta_product.html'
    context_object_name = 'meta_product'
    model = MetaProduct

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        cart_item = set_initial_cart_status(request=self.request)
        cart_items = cart_item.get('cart_items')
        form = ProductOpinionForm()
        viewed_meta_product = get_object_or_404(MetaProduct, id=self.kwargs['meta_product_id'])
        products = viewed_meta_product.product_set.all()
        opinions = ProductOpinion.objects.filter(product=viewed_meta_product)
        context = {'categories': categories,
                   'meta_product': viewed_meta_product,
                   'products': products,
                   'form': form,
                   'opinions': opinions,
                   'cart_items': cart_items}
        return context


def orders_history(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        user_orders = Order.objects.filter(customer=customer, complete=True)
        context = {'customer': customer, 'user_orders': user_orders}
        return render(request, 'orders_history.html', context)


def order_history(request, user_order_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        history_order = Order.objects.get(customer=customer, id=user_order_id)
        history_items = history_order.get_orderitems

        context = {'history_order': history_order, 'history_items': history_items}
        return render(request, 'order_history.html', context)


def favourites(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        user_favourites = FavouriteProduct.objects.filter(customer=customer, favourite=True)
        context = {'user_favourites': user_favourites, 'cart_items': cart_items}
        return render(request, 'favourites.html', context)
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    #     cart_items = order['get_cart_items']




