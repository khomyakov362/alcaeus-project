from django.views.generic import ListView

from books.models import Book


class BooksListView(ListView):
    model = Book
    paginate_by = 10
    extra_contenxt = {
        'title': 'Books List'
    }
    template_name = 'books/list.html'

