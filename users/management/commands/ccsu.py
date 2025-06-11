from os import getenv
from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        admin_user = User.objects.create(
            username=getenv('SITE_ADMIN_USERNAME'),
            email=getenv('SITE_ADMIN_EMAIL'),
            role='admin',
            description='The site administator.',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        admin_user.set_password(getenv('SITE_ADMIN_PASSWORD'))
        admin_user.save()
        print('Admin created')
    