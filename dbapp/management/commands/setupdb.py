from subprocess import run

from django.core.management import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *args, **options):

        migrations_args_lists = list(map(
            lambda el: ['py', 'manage.py', 'makemigrations', el],
            settings.CUSTOM_APPS
        ))

        args_lists = [['py', 'manage.py', 'ccdb']] + (
        migrations_args_lists +
        [
            ['py', 'manage.py', 'migrate'],
            ['py', 'manage.py', 'ccsu'],
            ['py', 'manage.py', 'clonerepo'],
            ['py', 'manage.py', 'loadbooks'],
        ])

        for list_ in args_lists:
            proc = run(list_)
            if proc.returncode != 0:
                raise RuntimeError(f'The subprocess with arguments "{' '.join(list_)}" '
                                    'ended with an unexpected error.\n'
                                   f'Return code: {proc.returncode}')
  

        print('\nSetup is finished. Ready to work with the project.')
