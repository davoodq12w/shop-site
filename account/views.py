from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
            address.save()
            return redirect('shop:product_list')
    else:
        form = AddressForm()
    return render(request, 'forms/add_address.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    saves = user.saves.all()
    context = {
        'saves': saves,
        'user': user,
    }
    return render(request, 'shop/profile.html', context)


@login_required()
def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f" name:{cd['name']}\n phone:{cd['phone']}\n email:{cd['email']}\n\n {cd['message']}"
            send_mail(
                cd['subject'],
                message,
                'davodrashiworking@gmail.com',
                ['davod.q12w@gmail.com'],
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
    return render(request, 'shop/comments.html', {'comments': comments})


@login_required
def saved_products(request):
    products = request.user.saves.all()
    return render(request, 'shop/saved_products.html', {'products': products})


@login_required
def user_addresses(request):
    addresses = request.user.addresses.all()
    return render(request, 'shop/addresses.html', {'addresses': addresses})


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


