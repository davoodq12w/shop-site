from django.contrib.auth import get_user_model
from django.db import models
from django_resized import ResizedImageField
from django_jalali.db import models as jmodels

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(max_length=2000)
    price = models.PositiveIntegerField()
    off = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(default=0)
    inventory = models.PositiveIntegerField()
    weight = models.PositiveIntegerField(default=0)
    created = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    rate = models.FloatField(default=3.0)
    sells = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created', 'name', '-update']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-update']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class ProductFeatures(models.Model):
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=500)
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name}: {self.value}"


def image_sorter(instance, filename):
    return f"product_images/{instance.created.year}/{instance.created.month}/{instance.created.day}/{filename}"


class Image(models.Model):
    title = models.CharField(max_length=250)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    created = jmodels.jDateTimeField(auto_now_add=True)
    file = ResizedImageField(upload_to=image_sorter)

    class Meta:
        ordering = ['title', '-created']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['-created']),
        ]


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    bad = models.BooleanField(default=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = jmodels.jDateTimeField(auto_now_add=True)
    rate = models.IntegerField()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name}"
