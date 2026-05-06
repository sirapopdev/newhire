from django.contrib import admin

# Register your models here.
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']

admin.site.register(Category, CategoryAdmin)