from django.db.models.signals import *
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender=Product)
def price_update(sender, instance, **kwargs):
    instance.discount_price = instance.price - instance.off
