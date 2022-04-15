from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
<<<<<<< HEAD
    path('list/', views.list_view, name='list'),
    path('list/<int:crystal_id>/', views.result_hkl_view_by_id, name=''),
    # path('list/<str:crystal_formula>/', views.result_hkl_view_by_id, name='list'),
    path('hkl-crystal/', views.hkl_crystal_view, name='hkl-crystal'),

=======
>>>>>>> work-branch
    path('home/', views.home_view, name='home'),
    path('upload-cif-file/', views.upload_cif_file, name='upload_cif_file'),
    path('forms/', views.crystal_data_create_view, name='submit'),
    path('database-search/', views.database_search_view, name='database_search'),
    path('database-search/<int:crystal_id>/',
         views.result_hkl_view_by_id, name='list'),
    path('database-search/<int:crystal_id>/update/',
         views.update_crystal_data_view, name="update"),
    path('database-search/<int:crystal_id>/delete/',
         views.delete_crystal_data_view, name="delete"),
     path('database-search/<int:crystal_id>/cif-display/',
         views.cif_file_display, name="cif_display"),

]
