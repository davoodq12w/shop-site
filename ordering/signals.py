from django.db.models.signals import *
from django.dispatch import receiver
from .models import *
from cart.kavenegar.send_sms_to_user import *


@receiver(pre_save, sender=Order)
def status_sender(sender, instance, **kwargs):

    phone = instance.buyer.phone
    order_status = instance.status
    message = None

    if order_status == 'Processing':
        message = 'مشترک گرامی سفارش شما در حال بررسی است'
    elif order_status == 'Sending':
        message = "مشترک گرامی سفارش شما برایتان ارسال شده است"
    elif order_status == 'Received':
        message = "مشترک گرامی رسیدن بسته به شما تایید شد امید وارم از سفارشتون راضی باشید"
    elif order_status == 'Rejected':
        message = "مشترک گرامی مرجوعیت شما با موفقیت انجام شد با تشکر "
    if message:
        # sms(phone, message)
        print(f'{phone}\n {message}')
