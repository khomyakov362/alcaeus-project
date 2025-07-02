from django.contrib import admin
from books.models import Book, FavouriteBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'language')
    ordering = ('pk', 'title', 'author')

@admin.register(FavouriteBook)
class FavouriteBook(admin.ModelAdmin):
    list_display = ('book', 'user',)
    ordering = ('user',)
