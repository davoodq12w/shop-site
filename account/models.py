from django.utils import timezone
from shop.models import Product
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_jalali.db import models as jmodels


class ShopUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('phone must be exist')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields['is_superuser'] is not True:
            raise ValueError('You must set is_superuser True')

        if extra_fields['is_staff'] is not True:
            raise ValueError('You must set is_staff True')

        return self.create_user(phone, password, **extra_fields)


class ShopUser(PermissionsMixin, AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = jmodels.jDateTimeField(default=timezone.now)
    saves = models.ManyToManyField(Product, related_name='user_saves', blank=True)

    objects = ShopUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(ShopUser, related_name='addresses', on_delete=models.CASCADE)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    exact_address = models.TextField()
    postal_code = models.CharField(max_length=10, unique=True)
    receiver_name = models.CharField(max_length=50)
    receiver_phone = models.CharField(max_length=11)

    def __str__(self):
        return (f'استان: {self.province} '
                f'شهر: {self.city} '
                f'کد پستی: {self.postal_code} ')


class Ticket(models.Model):

    class Subject(models.TextChoices):
        CRITICISM = 'C', 'criticism'
        PROPOSAL = 'P', 'proposal'
        REPORT = 'R', ' report'

    subject = models.CharField(max_length=1, choices=Subject.choices)
    message = models.TextField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=200)