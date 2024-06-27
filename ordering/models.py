from django.db import models
from shop.models import Product
from django_jalali.db import models as jmodels
from account.models import ShopUser
# Create your models here.


class Order(models.Model):

    class Status(models.TextChoices):
        NONE = ('None', 'خالی')
        PROCESSING = ('Processing', ' در حال پردازش ')
        SENDING = ('Sending', 'درحال ارسال')
        RECEIVED = ('Received', 'دریافت شده')
        REJECTED = ('Rejected', 'مرجوع')

    buyer = models.ForeignKey(ShopUser, related_name='orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=250)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    reference_id = models.CharField(null=True, blank=True)
    status = models.CharField(choices=Status.choices,default=Status.NONE)

    def __str__(self):
        return f"order by id {self.id}"

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=['-created']),
        ]

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight < 500:
            return 0
        elif 500 <= weight < 1000:
            return 20000
        elif 1000 <= weight < 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        return self.get_post_cost() + self.get_total_cost()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"product:{self.product}, quantity:{self.quantity}, price:{self.price}"

    def get_cost(self):
        return self.quantity * self.price

    def get_weight(self):
        return self.quantity * self.weight


class Payment(models.Model):
    tracking_code = models.CharField()
    payer = models.ForeignKey(ShopUser, related_name='payments', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField()
    created = jmodels.jDateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"tracking_code: {self.tracking_code}"
