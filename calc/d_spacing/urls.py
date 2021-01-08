from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('list/', views.list_view, name='list'),
    path('list/<int:crystal_id>/', views.result_hkl_view_by_id, name='list'),    
    path('hkl-crystal/', views.hkl_crystal_view, name='hkl-crystal'),

    
    path('forms/', views.crystal_data_create_view, name='submit'),
    path('database/', views.database_view, name='database'),
    path('database/<int:crystal_id>/', views.result_hkl_view_by_id, name='list'),

]
