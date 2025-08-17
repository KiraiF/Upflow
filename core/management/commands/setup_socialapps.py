from django.core.management.base import BaseCommand
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = "Sets up Google and GitHub SocialApps"

    def handle(self, *args, **kwargs):
        site = Site.objects.get_or_create(id=1, defaults={"domain": "localhost", "name": "localhost"})[0]

        if not SocialApp.objects.filter(provider="google").exists():
            google_app = SocialApp.objects.create(
                provider="google",
                name="Google",
                client_id=settings.GOOGLE_CLIENT_ID,
                secret=settings.GOOGLE_SECRET,
            )
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS("Google app created."))

        if not SocialApp.objects.filter(provider="github").exists():
            github_app = SocialApp.objects.create(
                provider="github",
                name="GitHub",
                client_id=settings.GITHUB_CLIENT_ID,
                secret=settings.GITHUB_SECRET,
            )
            github_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS("GitHub app created."))

        self.stdout.write(self.style.SUCCESS("Social apps set up successfully."))