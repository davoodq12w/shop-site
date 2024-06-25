from django.urls import path
from . import views


app_name = 'ordering'

urlpatterns = [
    path('verify_phone', views.verify_phone, name='verify_phone'),
    path('verify_code', views.verify_code, name='verify_code'),
    path('create_order', views.create_order, name='create_order'),
    path('load_address', views.load_address, name='load_address'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('download_order_pdf/<int:order_id>', views.download_order_pdf, name='download_order_pdf'),
]
