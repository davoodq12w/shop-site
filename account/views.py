from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
