from django.db import models
from django_resized import ResizedImageField
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
    discount_price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

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
        return f"{self.name}:{self.value}"


def image_sorter(instance, filename):
    return f"product_images/{instance.created.year}/{instance.created.month}/{instance.created.day}/{filename}"


class Image(models.Model):
    title = models.CharField(max_length=250)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    file = ResizedImageField(upload_to=image_sorter)

    class Meta:
        ordering = ['title', '-created']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['-created']),
        ]
