from django.conf import settings
from django.db import models
from users.models import NULLABLE, User


class Book(models.Model):

    title = models.CharField(max_length=150, verbose_name='title', **NULLABLE)
    author = models.CharField(max_length=50, verbose_name='author', **NULLABLE)
    editor = models.CharField(max_length=50, verbose_name='editor', **NULLABLE)
    translator = models.CharField(max_length=100, verbose_name='translator', **NULLABLE)
    date = models.CharField(max_length=50, verbose_name='date', **NULLABLE)
    directory_path = models.CharField(max_length=50, verbose_name='directory path')
    file_name = models.SlugField(max_length=50, verbose_name='file name', unique=True, db_index=True)
    language = models.CharField(max_length=10, verbose_name='language', **NULLABLE)
    xml_data = models.TextField(verbose_name='xml data')
    html_data = models.TextField(verbose_name='html data', **NULLABLE)   

    def __str__(self):
        return str(self.title)

    @property
    def cts_urn(self) -> str:
        string = self.file_name.replace('-', '.')

        for key in settings.LANG_VALUES.keys():
            string = string.replace(f'.{key}', f'-{key}')

        return settings.CTS_URN_PREFIX + string
    
    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'


class FavouriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='book')

    class Meta:
        verbose_name = 'favourite book'
        verbose_name_plural = 'favourite books'
