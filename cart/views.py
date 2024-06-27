from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from django.http import JsonResponse
from .cart import Cart
# Create your views here.


@require_POST
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product)
        context = {
            'length': len(cart),
            'total_price': cart.get_total_price(),
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'error': 'error'})


def cart_detail(request):
    cart = Cart(request)
    empty_cart = False
    if request.session['cart'] == {} or request.session['cart'] is None:
        empty_cart = True

    context = {
        'cart': cart,
        'empty_cart': empty_cart,
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def update_quantity(request):
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    if action == 'add':
        cart.add(product)
    elif action == 'minus':
        cart.decrease(product)
    price = product.discount_price
    context = {
        'product_total_price': price * cart.cart[product_id]['quantity'],
        'product_quantity': cart.cart[product_id]['quantity'],
        'length': len(cart),
        'total_price': cart.get_total_price(),
        'final_price': cart.get_final_price(),
        'post_price': cart.get_post_price(),
    }
    return JsonResponse(context)


@require_POST
def remove_product(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    context = {
        'length': len(cart),
        'total_price': cart.get_total_price(),
        'final_price': cart.get_final_price(),
        'post_price': cart.get_post_price(),
    }
    return JsonResponse(context)


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")

