from shutil import rmtree

from django.core.management import BaseCommand, CommandError
from django.conf import settings

from books.management.rmtree_error_handler import handleRemoveReadonly

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        if not settings.TEMP_FOLDER.exists():
            raise CommandError(f'The temporary folder at {settings.TEMP_FOLDER} does not exist.')
        
        rmtree(settings.TEMP_FOLDER, False, onexc=handleRemoveReadonly)

        print(f'The folder at {settings.TEMP_FOLDER} has been deleted.')
