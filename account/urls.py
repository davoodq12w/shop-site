from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add_address', views.add_address, name='add_address'),
    path('profile', views.profile, name='profile'),
    path('ticket/', views.ticket, name='ticket'),
    path('user_comments/', views.user_comments, name='user_comments'),
    path('saved_products/', views.saved_products, name='saved_products'),
    path('addresses/', views.user_addresses, name='addresses'),

    # =====================================
    # for password reset
    # =====================================
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # =====================================
    # for password change
    # =====================================
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

]
