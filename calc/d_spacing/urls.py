from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('database-search/', views.database_search_view, name='database_search'),
    path('home/', views.home_view, name='home'),
    # path('list/', views.list_view, name='list'),
    # path('list/<int:crystal_id>/', views.result_hkl_view_by_id, name='list'),
    # path('hkl-crystal/', views.hkl_crystal_view, name='hkl-crystal'),    
    # path('database/', views.database_view, name='database'),
    path('database-search/<int:crystal_id>/', views.result_hkl_view_by_id, name='list'),    
    path('forms/', views.crystal_data_create_view, name='submit'),
    path('update/<int:crystal_id>/', views.update_crystal_data_view, name='update'),
    path('delete/<int:crystal_id>/', views.delete_crystal_data_view, name='delete'),
]
