from django.urls import path

from . import views


app_name = 'account'


urlpatterns = [
    path('home', views.account_home_view, name='account-home'),



]
