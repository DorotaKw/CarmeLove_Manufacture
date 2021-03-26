from django.views.generic import DetailView

from .models import Article

from store.models import Category
from store.views import set_initial_cart_status


class AboutCarmeLoveView(DetailView):
    model = Article
    template_name = 'about_carmelove.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = set_initial_cart_status(request=self.request)
        cart_items = cart_item.get('cart_items')
        context.update({
            'categories': Category.objects.all(),
            'articles': Article.objects.all(),
            'cart_items': cart_items,
        })
        return context
