from django.contrib import admin
from books.models import Book


admin.register(Book)
class Book:
    list_display = ('pk', 'title', 'author', 'language')
    ordering = ('pk', 'title', 'author')
