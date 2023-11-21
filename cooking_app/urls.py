from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view_all/', views.view_all, name='recipes'),
    path('about/', views.about, name='about'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('view_recipe/<int:recipe_id>', views.view_recipe, name='view_recipe'),
    path('upload_recipe/', views.upload_recipe, name='upload_recipe'),
    path('edit_recipe/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('edit_image/<int:recipe_id>', views.edit_image, name='edit_image'),
    path('delete_recipe/<int:recipe_id>', views.delete_recipe, name='delete_recipe'),

]
