from pathlib import Path
from shutil import rmtree
from subprocess import run

from django.conf import settings
from django.core.management import BaseCommand

from books.management.rmtree_error_handler import handleRemoveReadonly


class Command(BaseCommand):

    @staticmethod
    def _ensure_dir_exists_and_empty(direc: Path):
        
        if not direc.exists():
            direc.mkdir()
        elif len(list(direc.iterdir())) > 0:
            rmtree(direc, False, onexc=handleRemoveReadonly)
            direc.mkdir()
        
    def handle(self, *args, **options):

        Command._ensure_dir_exists_and_empty(settings.TEMP_FOLDER)

        run(['git', 'clone', '--depth', '1', settings.BOOKS_REPO, settings.TEMP_FOLDER])

        print(f'The repository {settings.BOOKS_REPO} has been cloned to {settings.TEMP_FOLDER}.')
