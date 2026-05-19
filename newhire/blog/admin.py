from django.contrib import admin

# Register your models here.
from .models import Category, Comment, Post, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


admin.site.register(Tag, TagAdmin)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'created_at', 'updated_at']
    search_fields = ['title', 'slug', 'category', 'created_at', 'updated_at']
    list_filter = ['category', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'body', 'created_at']
    search_fields = ['author', 'post', 'body', 'created_at']


admin.site.register(Comment, CommentAdmin)
