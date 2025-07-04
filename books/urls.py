from django.urls import path

from books.apps import BooksConfig
from books import views

app_name = BooksConfig.name


urlpatterns = [
    path('', views.BooksListView.as_view(), name='books_list'),
    path('<slug:file_name>/detail/',
         views.BookDetailView.as_view(),
         name='book_detail'),
    path('<slug:file_name>/doc/',
         views.PlainDocView.as_view(),
         name='book_plain_doc'),
    path('<slug:file_name>/download/', 
         views.DownloadDocView.as_view(),
         name='book_download_doc'),
    path('add-favourite/', 
         views.AddFavouriteView.as_view(),
         name='book_add_favourite'),
    path('<int:pk>/remove-favourite/',
         views.RemoveFavouriteView.as_view(),
         name='remove_favourite'),
    path('<int:pk>/remove-favourite-detail/', 
         views.RemoveFromBookDetailView.as_view(), 
         name='remove_favourite_detail'),
    path('favourite-list/',
         views.FavouriteListView.as_view(),
         name='favourite_list'),
]
