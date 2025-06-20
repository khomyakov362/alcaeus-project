from django.urls import path

from books.apps import BooksConfig
from books import views

app_name = BooksConfig.name


urlpatterns = [
    path('list/', views.BooksListView.as_view(), name='books_list'),

]
