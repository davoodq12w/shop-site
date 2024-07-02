from django.urls import path
from . import views


app_name = 'ordering'

urlpatterns = [
    path('verify_phone', views.verify_phone, name='verify_phone'),
    path('verify_code', views.verify_code, name='verify_code'),
    path('create_order', views.create_order, name='create_order'),
    path('load_address', views.load_address, name='load_address'),
    path('request/', views.send_request, name='request'),
    path('request/<int:id>/', views.send_request, name='reset_payment'),
    path('verify/', views.verify, name='verify'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('download_order_pdf/<int:order_id>', views.download_order_pdf, name='download_order_pdf'),
    path('reject_product/<int:product_id>', views.reject_product, name='reject_product'),
    path('add_image/', views.reject_product, name='add_image'),
    path('reject_details/<int:reject_id>', views.reject_details, name='reject_details'),
]
