from django.db import models
from bs4 import BeautifulSoup
from users.models import NULLABLE


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
    
    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    @property 
    def xml_header(self) -> str | None:
        bs = BeautifulSoup(str(self.xml_data), 'xml')
        header = bs.find('teiHeader')

        if header:
            return header.prettify()
    
    # @property
    # def table_of_contents(self) -> tuple[str, tuple[str, ...]]:

