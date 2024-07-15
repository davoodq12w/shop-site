from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('products_api/', views.ProductListApi.as_view(), name='products_api'),
    path('product_details_api/<int:pk>', views.ProductDetailsApi.as_view(), name='product_details_api'),
]
