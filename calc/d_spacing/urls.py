from django.urls import path

from . import views

app_name = 'd_spacing'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('upload-cif-file/', views.upload_cif_file_view, name='upload_cif_file'),
    path('forms/', views.crystal_data_create_view, name='crystal_data_create'),
    path('database-search/', views.database_search_view, name='database_search'),
    path('database-search/<int:crystal_id>/',
         views.dspaing_results_view, name='dspaing_results'),
    path('database-search/<int:crystal_id>/update/',
         views.update_crystal_data_view, name="update_crystal_data"),
    path('database-search/<int:crystal_id>/delete/',
         views.delete_crystal_data_view, name="delete_crystal_data"),
     path('database-search/<int:crystal_id>/cif-display/',
         views.cif_file_display, name="cif_display"),

]
