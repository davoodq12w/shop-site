from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add_address', views.add_address, name='add_address'),
    path('profile', views.profile, name='profile'),
]
