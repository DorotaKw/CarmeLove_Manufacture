from django.shortcuts import render

from .models import Article
from store.models import Category
from store.utils import cart_data


def about_us(request):
    data = cart_data(request)

    cart_items = data['cart_items']

    categories = Category.objects.all()
    o_nas = Article.objects.get(title_main='O Nas')
    context = {'categories': categories, 'cart_items': cart_items,
               'o_nas': o_nas}
    return render(request, 'about_us.html', context)

