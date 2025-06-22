from django.views.generic import ListView
from django.db.models import Q

from books.models import Book


class BooksListView(ListView):
    model = Book
    paginate_by = 30
    extra_contenxt = {
        'title': 'Books List',
    }
    queryset = Book.objects.order_by('title')

    def get_queryset(self):
        author = self.request.GET.get('author')
        title = self.request.GET.get('title')
        lang = self.request.GET.get('lang')
        if lang:
            langs = ['latin', 'english', None, '']
        else:
            langs = [lang]

        if author and title:
            return Book.objects.filter(
                Q(title__icontains=title) &
                Q(author__icontains=author) &
                Q(language__in=langs)
            )
        
        if author:
            return Book.objects.filter(
                Q(author__icontains=author) &
                Q(language__in=langs)
            )

        if title:
            return Book.objects.filter(
                Q(title__icontains=title) &
                Q(language__in=langs)
            )
        
        else:
            return super().get_queryset()

    template_name = 'books/list.html'
