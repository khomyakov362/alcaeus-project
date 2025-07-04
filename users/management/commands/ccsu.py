from os import getenv
from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):

    help = """Command to Create Super User. Creates admin user inside the database with email,
username and password provided in the .env file."""

    def handle(self, *args, **options):
        admin_user = User.objects.create(
            username=getenv('SITE_ADMIN_USERNAME'),
            email=getenv('SITE_ADMIN_EMAIL'),
            role='admin',
            description='The site administrator.',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        admin_user.set_password(getenv('SITE_ADMIN_PASSWORD'))
        admin_user.save()
        print('Admin created')
    