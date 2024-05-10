from django.contrib import admin
from .models import *
# Register your models here.


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class ProductFeaturesInline(admin.StackedInline):
    model = ProductFeatures
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'inventory', 'created', 'category',]
    list_filter = ['category', 'created', 'inventory']
    search_fields = ['name', 'price', 'created']
    prepopulated_fields = {'slug': ['name']}
    inlines = [ProductFeaturesInline, ImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ['name']}
