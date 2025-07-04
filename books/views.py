from django.http import (
    HttpResponse, 
    HttpResponseRedirect,
    Http404
)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    DeleteView
)
from django.db.models import Q
from django.conf import settings

from books.models import Book, FavouriteBook

languages = list(settings.LANG_VALUES.values())


class BooksListView(ListView):
    model = Book
    paginate_by = 30
    template_name = 'books/list.html'
    extra_context = {
        'title': 'Books List',
        'languages': languages
    }

    def get_queryset(self):
        author = self.request.GET.get('author')
        title = self.request.GET.get('title')
        lang = self.request.GET.get('lang')
        if not lang:
            langs = [None] + languages
        else:
            langs = [lang]
        order_by = self.request.GET.get('orderby')
        if not order_by:
            order_by = 'title'

        if author and title:
            return Book.objects.filter(
                Q(title__icontains=title) &
                Q(author__icontains=author) &
                Q(language__in=langs)
            ).order_by(order_by)
        
        if author:
            return Book.objects.filter(
                Q(author__icontains=author) &
                Q(language__in=langs)
            ).order_by(order_by)

        if title:
            return Book.objects.filter(
                Q(title__icontains=title) &
                Q(language__in=langs)
            ).order_by(order_by)
        
        else:
            return Book.objects.filter(language__in=langs).order_by(order_by)


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/detail.html'
    slug_field = 'file_name'
    slug_url_kwarg = 'file_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_ = self.get_object()

        if self.request.user.is_authenticated:
            try:
                favourite = FavouriteBook.objects.get(
                    book=object_,
                    user=self.request.user
                )
            except FavouriteBook.DoesNotExist:
                favourite = None
        else: favourite = None

        associated_books = Book.objects.filter(
            Q(directory_path=object_.directory_path) & 
            ~ Q(pk=object_.pk)
        )

        context['title'] = object_.title + 'Details'
        context['associated_books'] = associated_books
        context['favourite'] = favourite

        return context


class PlainDocView(DetailView):
    model = Book
    slug_field = 'file_name'
    slug_url_kwarg = 'file_name'

    def get(self, request, *args, **kwargs):

        if self.request.GET.get('rawXml') == 'true':
            plain_content = self.get_object().xml_data
            content_type = 'text/xml'
        else:
            plain_content = self.get_object().html_data
            content_type = None

        return HttpResponse(plain_content, content_type=content_type)
        

class DownloadDocView(DetailView):
    model = Book
    slug_field = 'file_name'
    slug_url_kwarg = 'file_name'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if self.request.GET.get('rawXml') == 'true':
            plain_content = obj.xml_data
            name = obj.file_name + '.xml'
            type_ = 'text/xml'
        else:
            plain_content = obj.html_data
            name = obj.file_name + '.html'
            type_ = 'text/xhtml'

        return HttpResponse(
            plain_content, 
            headers={
            "Content-Type": f"{type_}",
            "Content-Disposition": f'attachment; filename="{name}"',
            })
    

class AddFavouriteView(CreateView):
    model = FavouriteBook

    def post(self, request, *args, **kwargs):

        if self.request.POST:
            user = self.request.user
            book_pk = self.request.POST.get('book_pk')
            book = Book.objects.get(pk=book_pk)
            self.model.objects.get_or_create(user=user, book=book)
            return HttpResponseRedirect(reverse_lazy(
                'books:book_detail', 
                kwargs={'file_name': book.file_name}
                ))
    

class RemoveFavouriteView(DeleteView):
    model = FavouriteBook
    success_url = reverse_lazy('books:favourite_list')

    def get_object(self, queryset = ...):
        object_ = super().get_object()
        if object_.user != self.request.user:
            raise Http404
        
        return object_
    

class RemoveFromBookDetailView(RemoveFavouriteView):
    success_url = None

    def get_success_url(self):

        return reverse_lazy(
            'books:book_detail', 
            kwargs={'file_name': self.get_object().book.file_name})
                

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        book = self.object.book
        self.object.delete()

        return HttpResponseRedirect(reverse_lazy(
            'books:book_detail', 
            kwargs={'file_name': book.file_name}
            ))


class FavouriteListView(ListView):

    model = FavouriteBook
    template_name = 'books/favourite_list.html'
    extra_context = {
        'title': 'Your Favourite Books',
    }

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        
        return self.model.objects.filter(
            user=self.request.user
        )
