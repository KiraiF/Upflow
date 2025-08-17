from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser from environment variables if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()

        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if not admin_username or not admin_email or not admin_password:
            self.stderr.write("ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD must be set in environment.")
            return

        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(f"Superuser {admin_username} already exists.")
        else:
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(f"Superuser {admin_username} created.")
