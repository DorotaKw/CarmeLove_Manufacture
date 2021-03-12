import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView

# from django.contrib.auth.middleware import A

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin

from .models import Customer, Category, Product, Order, OrderItem, ProductOpinion, MetaProduct, OrderComment
from .forms import ProductOpinionForm, OrderCommentForm

from .utils import *


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def check_user_auth(request):
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
    about = 'Hi! We are small Manufacture of Sweets!'
    context = {'categories': categories, 'cart_items': cart_items, 'about': about}
    return render(request, 'home.html', context)


# class HomeView(ListView):
#     template_name = 'home.html'
#     about = 'Hi! We are small Manufacture of Sweets!'
#     context_object_name = 'about'


class StoreView(ListView):
    template_name = 'store.html'
    context_object_name = 'meta_products'
    model = MetaProduct

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = check_user_auth(request=self.request)
        cart_items = cart_item.get('cart_items')
        context.update({
            'categories': Category.objects.all(),
            'cart_items': cart_items,
        })
        return context

    def get_queryset(self):
        return MetaProduct.objects.all().order_by('name')


class CategoryDetailView(DetailView):
    template_name = 'category.html'
    context_object_name = 'categories'
    model = Category

    # def get_object(self, queryset=None):
    #     viewed_category = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
    #     meta_products = get_object_or_404(MetaProduct, category=self.kwargs.get('category_id'))
    #     context = {'viewed_category': viewed_category, 'meta_products': meta_products}
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = check_user_auth(request=self.request)
        cart_items = cart_item.get('cart_items')
        # viewed_category = get_object_or_404(Category, id=self.request.GET.get['pk'])
        # meta_products = get_object_or_404(MetaProduct, category=self.request.GET.get['pk'])
        viewed_category = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        meta_products = get_object_or_404(MetaProduct, category=self.kwargs.get('category_id'))
        #viewed_category = Category.objects.get(id=category_id)
        #meta_products = MetaProduct.objects.filter(category=self.category_id).order_by('name').all()

        context.update({
            'viewed_category': viewed_category,
            'meta_products': meta_products,
            'cart_items': cart_items
        })
        return context

    def get_queryset(self):
        return Category.objects.all().order_by('name')

"""
class MyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use kwargs from URL
        context['first_object'] = get_object_or_404(FirstObjectModel, id=self.kwargs['pk'])
        context['second_object'] = get_object_or_404(SecondObjectModel, id=self.kwargs['abc'])
        # Fetch from GET params
        context['first_object'] = get_object_or_404(FirstObjectModel, id=self.request.GET.get('pk'))
        context['second_object'] = get_object_or_404(SecondObjectModel, id=self.request.GET.get('abc'))
        return context
        """


# def category(request, category_id):
#     data = cart_data(request)
#     cart_items = data['cart_items']
#
#     categories = Category.objects.all()
#     viewed_category = Category.objects.get(id=category_id)
#     meta_products = MetaProduct.objects.filter(category=category_id).order_by('name').all()
#     context = {'categories': categories, 'viewed_category': viewed_category,
#                'meta_products': meta_products, 'cart_items': cart_items}
#     return render(request, 'category.html', context)


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
    data = cart_data(request)
    cart_items = data['cart_items']

    if request.user.is_authenticated:
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
        # for now it's the only idea I have, it's working, but view is too fat.
        # maybe JS or/and CSS will help?
        form = None

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


