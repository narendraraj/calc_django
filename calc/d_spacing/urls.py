from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('submit/', views.crystal_data_create_view, name='submit')
]
