from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('all/', views.all_recipes, name='all'),
    path('cookmarked/', views.cookmarked_recipes, name='index'),
    path('all/<int:recipe_id>/', views.recipe_details, name='details'),
    path('cookmarked/<int:recipe_id>/', views.my_recipe_details, name='mydetails'),
]
