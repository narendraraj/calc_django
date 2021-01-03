from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('list/', views.list_view, name='home'),
    path('hkl-crystal/', views.hkl_crystal_view, name='hkl-crystal'),
    
    path('home/', views.home_view, name='home'),
    path('forms/', views.crystal_data_create_view, name='submit')
]
