from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import *
from .forms import *
# Create your views here.


def create_user(request):
    if request.method == 'POST':
        form = ShopUserCreationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = ShopUser.objects.create(phone=cd['phone'])
            user.set_password(cd['password1'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            user = authenticate(request, phone=cd['phone'], password=cd['password1'])
            if user is not None:
                login(request, user)
                return redirect('shop:product_list')
            else:
                raise ValueError('user is not exist')
    else:
        form = ShopUserCreationForm()
    return render(request, 'forms/create_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = ShopLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone=cd['phone'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:product_list')
    else:
        form = ShopLoginForm()
    return render(request, 'forms/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('shop:product_list')


@login_required
def add_address(request):
    user = request.user
    if request.method == 'POST':
        form = AddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            if user.addresses.count() == 0:
                address.selected = True
            address.save()
            return redirect('account:addresses')
    else:
        form = AddressForm()
    return render(request, 'forms/add_address.html', {'form': form})


@login_required
def delete_address(request, address_id):
    user = request.user
    try:
        address = get_object_or_404(Address, id=address_id)
        if address.selected:
            address.delete()
            if user.addresses.count() > 0:
                next_address = user.addresses.first()
                next_address.selected = True
                next_address.save()
        else:
            address.delete()
        return redirect('account:addresses')
    except ValueError:
        return None


@require_POST
@login_required
def selection_address(request):
    address_id = request.POST.get('address_id')
    address = Address.objects.get(id=address_id)
    user = request.user
    if address:
        if user.addresses.filter(selected=True):
            selected = user.addresses.get(selected=True)
            selected.selected = False
            selected.save()
        else:
            return JsonResponse({'error': 'selected address is not available'})
        address.selected = True
        address.save()
    else:
        return JsonResponse({'error': 'address is not available'})
    data = {
        'selected_id': selected.id,
        'address_id': address.id,
    }
    return JsonResponse(data)


@login_required
def profile(request):
    user = request.user
    if not user.first_name:
        return redirect('account:edit_user')
    saves = user.saves.all()
    try:
        address = user.addresses.get(selected=True)
    except:
        address = None
    context = {
        'saves': saves,
        'user': user,
        'address': address,
    }
    return render(request, 'account/profile.html', context)


@login_required()
def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"نام: {cd['name']}\n شماره تماس: {cd['phone']}\n ایمیل: {cd['email']}\nمتن پیام:\n {cd['message']}"
            send_mail(
                cd['subject'],
                message,
                'davodrashiworking@gmail.com',
                [cd['email']],
                fail_silently=False
            )
            Ticket.objects.create(subject=cd['subject'], email=cd['email'], message=cd['message'], phone=cd['phone'],
                                  name=cd['name'],)
            return redirect('account:profile')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@login_required
def user_comments(request):
    comments = request.user.comments.all()
    return render(request, 'account/comments.html', {'comments': comments})


@login_required
def saved_products(request):
    products = request.user.saves.all()
    return render(request, 'account/saved_products.html', {'products': products})


@login_required
def user_addresses(request):
    addresses = request.user.addresses.all().order_by('-created')
    return render(request, 'account/addresses.html', {'addresses': addresses})


@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = ShopUserChangeForm(data=request.POST, instance=user)
        if form.is_valid():
            cd = form.cleaned_data
            user.phone = cd['phone']
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            return redirect('account:profile')
    else:
        form = ShopUserChangeForm(instance=user)

    return render(request, 'forms/edit_user.html', {'form': form})


@login_required
def user_orders(request):
    user = request.user
    orders = user.orders.all()
    return render(request, 'account/user_orders.html', {'orders': orders})


def orders_status(request, status):
    user = request.user
    orders = []
    if status == 'Processing':
         orders = user.orders.filter(status='Processing')
    elif status == 'Sending':
        orders = user.orders.filter(status='Sending')
    elif status == 'Received':
        orders = user.orders.filter(status='Received')
    elif status == 'rejected':
        orders = user.orders.filter(status='Rejected')
    else:
        orders = user.orders.all()
    return render(request, 'account/order_status.html', {'orders': orders})
