from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_by_category'),
    path('products/details/<slug:product_slug>/<int:id>/', views.product_details, name='product_details'),
    path('ordered_products/<slug:ordering_slug>/', views.product_list, name='product_ordering'),
    path('ordered_products/<slug:ordering_slug>/<slug:category_slug>/', views.product_list,
         name='product_ordering_by_category'),
    path('search/', views.search, name='search'),
    path('save/', views.save_product, name='save'),
    path('comment/', views.add_comment, name='comment'),
    path('rate/', views.rate, name='rate'),
]
