from django.urls import path

from books.apps import BooksConfig
from books import views

app_name = BooksConfig.name


urlpatterns = [
    path('', views.BooksListView.as_view(), name='books_list'),
    path('<slug:file_name>/detail/', views.BookDetailView.as_view(), name='book_detail'),
]
