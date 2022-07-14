from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('all/', views.all_recipes, name='all'),
    path('cookmarked/', views.cookmarked_recipes, name='index'),
    path('all/<int:recipe_id>/', views.recipe_details, name='details'),
    path('cookmarked/<int:recipe_id>/', views.my_recipe_details, name='mydetails'),
    path('cookmarked/create/', views.RecipeCreate.as_view(), name='recipe_create'),
    path('all/<int:recipe_id>/create/', views.YourRecipeCreate.as_view(), name='your_recipe_create'),
    path('cookmarked/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe_update'),
    path('cookmarked/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe_delete'),
    path('cookmarked/<int:recipe_id>/add_instruction/', views.add_instruction, name='add_instruction'),
    path('cookmarked/<int:recipe_id>/add_photo/', views.add_photo, name='add_photo'),
]
