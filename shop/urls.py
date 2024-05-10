from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_by_category'),
    path('products/details/<slug:product_slug>/<int:id>/', views.product_details, name='product_details'),
]
