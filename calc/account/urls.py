from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from account import views

app_name = 'account'


urlpatterns = [
    path('home', views.account_home_view, name='account_home'),
    path('login/', views.CustomLoginView.as_view(), name="account_login"),
    path('logout/', LogoutView.as_view(next_page='d_spacing:database_list'),
         name="account_logout"),
    # path('register/', views.account_register, name='account_register'),
    path('register/', views.CustomRegisterView.as_view(), name="account_register"),


    path('change-password/', auth_views.PasswordChangeView.as_view(),
         name="change_password"),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(),
         name="change_password_done"),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html' ),
         name="reset_password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name="password_reset_complete"),
]


