from django.contrib import admin
from .models import Category, Author, Book


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name']
    prepopulated_fields = {'slug': ['name']}


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    list_display = ['name', 'age']
    prepopulated_fields = {'slug': ['name']}


class BookAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'author']
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
