from django.contrib import admin
from .models import Recipe, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'ingredients')
    inlines = [CommentInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)

