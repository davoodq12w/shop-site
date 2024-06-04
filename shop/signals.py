from django.db.models.signals import *
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender=Product)
def price_update(sender, instance, **kwargs):
    instance.discount_price = instance.price - ((instance.price*instance.off)/100)
    instance.discount_price = instance.price - instance.off



@receiver(pre_save, sender=Comment)
def rate_update(sender, instance, **kwargs):
    rates = []
    for comment in instance.product.comments.all():
        if comment.rate != 0:
            rates.append(comment.rate)
    final_rate = round((sum(rates)/len(rates)), 1)
    instance.product.rate = final_rate
    instance.product.save()
