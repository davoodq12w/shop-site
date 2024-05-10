from django.shortcuts import render,get_object_or_404
from .models import *

# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/product_list.html', context)


def product_details(request, id, product_slug):
    product = get_object_or_404(Product, slug=product_slug, id=id)
    context = {
        'product': product
    }
    return render(request, 'shop/product_details.html', context)
