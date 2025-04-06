from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from .models import Recipe, Comment
from .forms import UserRegisterForm, RecipeForm, CommentForm, SearchForm

def home(request):
    """Home page view"""
    return render(request, 'recipes/home.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'recipes/signup.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})

@login_required
def add_recipe(request):
    """Add a new recipe view"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Your recipe has been added!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

def search_recipes(request):
    """Search recipes view"""
    form = SearchForm(request.GET)
    recipes = Recipe.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) | 
                Q(ingredients__icontains=query)
            )
        
        if category:
            recipes = recipes.filter(category=category)
    
    # If no search parameters, show some recommended recipes
    if not (query or category):
        recipes = recipes.order_by('-created_at')[:6]  # Show latest 6 recipes
    
    return render(request, 'recipes/search.html', {
        'form': form,
        'recipes': recipes,
        'is_search': bool(query or category)
    })

def recipe_detail(request, pk):
    """Recipe detail view"""
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all()
    
    # Handle new comment
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def edit_recipe(request, pk):
    """Edit recipe view"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if the user is the author
    if request.user != recipe.author:
        messages.error(request, 'You can only edit your own recipes!')
        return redirect('recipe_detail', pk=recipe.pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your recipe has been updated!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'recipes/logout.html')