from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random
from .models import *
from .forms import *
from cart.kavenegar.send_sms_to_user import *
from account.models import ShopUser
from django.contrib.auth import login
from cart.cart import Cart
from django.http import JsonResponse
from .renderers import render_to_pdf
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.conf import settings
from django.http import HttpResponse
import requests
import json
# Create your views here.


def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('ordering:create_order')
    if request.method == 'POST':
        form = VerifyPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            tokens = {'token': ''.join(random.choices('1234567890', k=5))}
            request.session['phone'] = phone
            request.session['verification_code'] = tokens['token']
            request.session['time_added_code'] = str(timezone.now())

            # verification(phone, tokens, 'verification')
            print(tokens)
            return redirect('ordering:verify_code')
    else:
        form = VerifyPhoneForm()
    return render(request, 'forms/verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        if code:

            if "time_added_code" in request.session:
                code_time_str = request.session["time_added_code"]
                code_time = parse_datetime(code_time_str)
                time_different = (timezone.now() - code_time).total_seconds()

                if time_different > 120:
                    del request.session['verification_code']
                    return redirect('ordering:verify_phone')

                else:
                    verification_code = request.session['verification_code']
                    phone = request.session['phone']
                    if code == verification_code:
                        user = ShopUser.objects.create(phone=phone)
                        password = f'{phone}shopsite'
                        user.set_password(password)
                        user.save()

                        message = (f'کاربر عزیز به سایت فروشگاهی خوش آمدید'
                                   f'جزییات حساب کاربری شما:'
                                   f'{phone}شماره تلفن : '
                                   f'{password}رمز شما: ')
                        # sms(phone, message)
                        print(message)
                        login(request, user)
                        del request.session['phone']
                        del request.session['verification_code']
                        del request.session['time_added_code']
                        return redirect('ordering:create_order')
    return render(request, 'forms/verify_code.html',)


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CreatOrderForm(request=request, data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                         price=item['price'], weight=item['weight'])
                request.session['order_id'] = order.id
            return redirect('ordering:request')
    else:
        form = CreatOrderForm(request=request)
    return render(request, 'ordering/create_order.html', {'form': form, 'cart': cart})


def load_address(request):
    address_id = request.POST.get('address_id')
    if address_id:
        address = Address.objects.get(id=address_id)
        data = {
            'name': address.receiver_name,
            'phone': address.receiver_phone,
            'province': address.province,
            'city': address.city,
            'postal_code': address.postal_code,
            'exact_address': address.exact_address,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'invalid address'})


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8000/ordering/verify/'


def send_request(request):
    order = Order.objects.get(id=request.session['order_id'])
    description = ""
    for item in order.items.all():
        description += item.product.name + " , "
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(request):
    cart = Cart(request)
    order = Order.objects.get(id=request.session['order_id'])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']

            if response_json['Status'] == 100:
                for item in order.items.all():
                    item.product.inventory -= item.quantity
                    item.product.save()
                order.paid = True
                order.reference_id = reference_id
                order.status = order.Status.PROCESSING
                order.save()
                payment_object = Payment.objects.create(payer=request.user, tracking_code=reference_id,
                                                        price=order.get_final_cost(), order=order)
                payment_object.save()
                cart.clear()
                return render(request, 'ordering/payment.html',
                              {"success": True, 'RefID': reference_id, "order_id": order.id})
            else:
                return render(request, 'ordering/payment.html',
                              {"success": False, })
        del request.session['order_id']
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.buyer == request.user:
        return render(request, 'ordering/order_detail.html', {'order': order})
    else:
        return render(request, 'ordering/not_your_order.html',)


@login_required
def download_order_pdf(request, order_id):
    order = Order.objects.get(id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factor_of_order_{order.id}.pdf"'
    response.write(render_to_pdf("pdf/order_factor.html", {'order': order},
                                 'ordering/templates/pdf/pdf_style.css'))
    return response
