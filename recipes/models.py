from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    steps = models.TextField()
    photo = CloudinaryField(upload_to='recipe_photos/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.recipe.title}'

