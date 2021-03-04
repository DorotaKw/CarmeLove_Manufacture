import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView

from .models import Customer, Category, Product, Order, OrderItem, ProductOpinion
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
    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}
    return render(request, 'store.html', context)


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


def product(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items

        # if request.method == 'GET':
        #     kwargs = {}
        #     kwargs['opinion_create'] = ProductOpinionForm(prefix='opinion_create')
        #     return render(request, 'product.html', kwargs)
        # elif request.method == 'POST':
        #     form = ProductOpinionForm(data=request.POST,
        #                               prefix='opinion_create')
        #     if form.is_valid():
        #         new_opinion = form.save(commit=False)
        #         new_opinion.user = request.user
        #         new_opinion.save()
        #         messages.success(request, 'Your opinion has been added successfully!')
        #         return HttpResponseRedirect('product',
        #                                     kwargs={
        #                                         'opinion_id': new_opinion.id
        #                                     })
        # messages.error(request, 'Invalid data, your opinion has not been saved.')
        # return HttpResponseRedirect(reverse('product'))
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']

    viewed_product = Product.objects.get(id=product_id)
    opinions = ProductOpinion.objects.filter(product=viewed_product)
    context = {'product': viewed_product, 'opinions': opinions, 'cart_items': cart_items}
    return render(request, 'product.html', context)


class ProductOpinionCreateView(CreateView):
    template_name = 'product.html'
    form_class = ProductOpinionForm
    success_url = reverse_lazy('product')
