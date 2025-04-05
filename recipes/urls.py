from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='recipes/logout.html'), name='logout'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
]

