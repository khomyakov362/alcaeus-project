from subprocess import run

from django.core.management import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):

        run(['py', 'manage.py', 'ccdb'])
        for each in settings.CUSTOM_APPS:
            run(['py', 'manage.py', 'makemigrations', each])
        run(['py', 'manage.py', 'migrate'])
        run(['py', 'manage.py', 'ccsu'])
        run(['py', 'manage.py', 'clonerepo'])
        run(['py', 'manage.py', 'loadbooks'])

        print('\nSetup is finished. Ready to work with the project.')
