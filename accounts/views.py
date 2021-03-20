from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from store.models import Customer, Order, OrderItem, FavouriteProduct

from .forms import SignUpForm


def hello(request):
    context = {'hello_message': 'Hi!'}
    return render(request, 'hello.html', context)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class SubmittableLoginView(LoginView):
    template_name = 'login_form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'login_form.html'
    success_url = reverse_lazy('store:home')


class SignUpView(CreateView):
    template_name = 'login_form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    context_object_name = 'history_order'
    model = Order

    def get_queryset(self):
        customer = self.request.user.customer
        return Order.objects.filter(customer=customer, complete=True)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'orders_items': history_order.get_orderitems,
    #     })
    #     return context


# view for Customer
def orders_history(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        user_orders = Order.objects.filter(customer=customer, complete=True)
        context = {'customer': customer, 'user_orders': user_orders}
        return render(request, 'orders_history.html', context)


# view for Customer
def order_history(request, user_order_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        history_order = Order.objects.get(customer=customer, id=user_order_id)
        history_items = history_order.get_orderitems

        context = {'history_order': history_order, 'history_items': history_items}
        return render(request, 'order_history.html', context)


# view for Customer
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


# view for Staff
class StaffView(StaffRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'staff.html'
    model = Order
    permission_required = 'accounts/.orders'


# view for Admin
class OrdersView(StaffRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'orders.html'
    model = Order
    permission_required = 'store/.orders'


# view for Admin
@staff_member_required
def order_details(request, order_details_id):
    viewed_order = Order.objects.get(id=order_details_id)
    order_items = viewed_order.get_orderitems
    order_comment = viewed_order.comment
    context = {'viewed_order': viewed_order, 'order_items': order_items, 'order_comment': order_comment}
    return render(request, 'order_details.html', context)


# view for Admin
class OrdersCompletedView(StaffRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'orders_completed.html'
    model = Order
    permission_required = 'accounts/.orders_completed'

    def get_queryset(self):
        return Order.objects.filter(complete=True)


# view for Admin
@staff_member_required
def completed_order_details(request, completed_order_details_id):
    viewed_order_completed = Order.objects.get(id=completed_order_details_id)
    order_items = viewed_order_completed.get_orderitems
    context = {'viewed_order_completed': viewed_order_completed, 'order_items': order_items}
    return render(request, 'completed_order_details.html', context)

