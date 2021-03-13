from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from store.models import Customer, Order, OrderItem

from .forms import SignUpForm


class SubmittableLoginView(LoginView):
    template_name = 'login_form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'login_form.html'
    success_url = reverse_lazy('home')


class SignUpView(CreateView):
    template_name = 'login_form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')


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

