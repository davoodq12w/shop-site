from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import *
from .forms import *


# Create your views here.


def product_list(request, ordering_slug=None, category_slug=None):
    def ordering_products(products_list, slug):
        if slug == 'inexpensive':
            return products_list.order_by('discount_price')
        if slug == 'expensive':
            return products_list.order_by('-discount_price')
        if slug == 'rate':
            return products_list.order_by('-rate')
        if slug == 'sells':
            return products_list.order_by('-sells')
        else:
            return products_list

    def ordering(slug):
        if slug == 'inexpensive':
            return 'ارزان ترین ها'
        if slug == 'expensive':
            return 'گران ترین ها'
        if slug == 'rate':
            return 'پرطرفدارترین ها'
        if slug == 'sells':
            return 'پرفروش ترین ها'
        else:
            return 'همه'

    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    if ordering_slug:
        products = ordering_products(products, ordering_slug)

    if request.headers.get('x-requested-with') == "XMLHttpRequest":
        price = request.POST.get('price')
        if price.isdigit():
            products = products.filter(discount_price__lt=int(price))

        return render(request, 'ajax/products.html', {"products": products})

    paginator = Paginator(products, 30)
    page_number = request.GET.get('page', 1)
    products = paginator.page(page_number)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'ordering_by': ordering(ordering_slug),
        'ordering_slug': ordering_slug,
    }
    return render(request, 'shop/product_list.html', context)


def product_details(request, id, product_slug):
    product = get_object_or_404(Product, slug=product_slug, id=id)
    recommended = product.category.products.exclude(id=product.id).order_by('-rate', '-sells')[:5]
    comments = product.comments.all()
    context = {
        'product': product,
        'recommended': recommended,
        'comments': comments,
    }
    return render(request, 'shop/product_details.html', context)


def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result1 = Product.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.1)
            result2 = Product.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(
                similarity__gt=0.1)
            result3 = Product.objects.annotate(similarity=TrigramSimilarity('slug', query)).filter(similarity__gt=0.1)
            results = (result1 | result2 | result3).order_by("-similarity")
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'shop/search_results.html', context)


@require_POST
@login_required
def save_product(request):
    user = request.user
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    if product in user.saves.all():
        user.saves.remove(product)
        saved = False
    else:
        user.saves.add(product)
        saved = True
    response_data = {
        'saved': saved,
    }
    return JsonResponse(response_data)


@login_required
@require_POST
def add_comment(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    text = request.POST.get('comment')
    rate = int(request.POST.get('rate'))
    comment = Comment.objects.create(product=product, author=request.user, text=text, rate=rate)
    comment.save()
    return render(request, 'ajax/comment_ajax.html', {'comment': comment})


@login_required
@require_POST
def rate(request):
    rate = int(request.POST.get('rate'))
    return render(request, 'ajax/rate-stars.html', {'rate': rate})
