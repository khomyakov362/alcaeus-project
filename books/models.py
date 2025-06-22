from django.db import models
from users.models import NULLABLE


class Book(models.Model):

    title = models.CharField(max_length=150, verbose_name='title', **NULLABLE)
    author = models.CharField(max_length=50, verbose_name='author', **NULLABLE)
    editor = models.CharField(max_length=50, verbose_name='editor', **NULLABLE)
    translator = models.CharField(max_length=100, verbose_name='translator', **NULLABLE)
    date = models.CharField(max_length=50, verbose_name='date', **NULLABLE)
    directory_path = models.CharField(max_length=50, verbose_name='directory path')
    file_name = models.CharField(max_length=50, verbose_name='file name')
    language = models.CharField(max_length=10, verbose_name='language', **NULLABLE)
    xml_data = models.TextField(verbose_name='xml data')

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    @staticmethod
    def _shorten(string: models.CharField) -> str:
        if string is None:
            return "\u2014"
        string = str(string).strip()
        if len(string) < 40:
            return string
        else:
            return string[0:37] + '...'

    @property
    def short_title(self) -> str:
        return Book._shorten(self.title)

    @property
    def short_author(self) -> str:
        return Book._shorten(self.author)
    
    @property
    def short_date(self) -> str: 
        if self.date is None:
            return "\u2014"
        return str(self.date).strip()[0:4]

    @property
    def cap_lang(self) -> str:
        if self.language is None:
            return "\u2014"
        return str(self.language).capitalize()




