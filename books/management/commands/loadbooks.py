from django.conf import settings
from django.core.management import BaseCommand

from books.xml_utils import generate_file_names, make_book_dict, send_to_convert
from books.models import Book


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        print('Starting loading boooks in the database...')

        paths = generate_file_names(settings.REPO_DATA_DIR)

        for path in paths:

            with open(path, 'rt', encoding='utf-8') as file:

                xml_str = file.read()

                book_dict = make_book_dict(path, settings.REPO_DATA_DIR, xml_str)

                file_name = book_dict['file_name']
                is_there = Book.objects.filter(file_name=file_name).exists()

                if is_there:
                    print(f'Book {book_dict["title"]} is already in the database')            
                    continue

                html = send_to_convert(settings.TEIGARAGE, xml_str)

                if not html:
                    html = None

                print(book_dict['title'])

                book = Book(
                    title=book_dict['title'],
                    author=book_dict['author'],
                    editor=book_dict['editor'],
                    translator=book_dict['translator'],
                    date=book_dict['date'],
                    directory_path=book_dict['directory_path'],
                    file_name=book_dict['file_name'],
                    language=book_dict['language'],
                    xml_data=xml_str,
                    html_data=html
                )

                book.save()
        
        print('The books have been loaded successfully.')



