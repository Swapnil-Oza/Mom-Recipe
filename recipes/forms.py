from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'steps', 'photo', 'category']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'steps': forms.Textarea(attrs={'rows': 10}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, 
                           widget=forms.TextInput(attrs={'placeholder': 'Search recipes...'}))
    category = forms.ChoiceField(choices=[('', 'All Categories')] + Recipe.CATEGORY_CHOICES, required=False)

