from accounts.models import AccountCode
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "Clear account codes that are older than 14 days"

    def handle(self, *args, **options):
        AccountCode.objects.filter(
            created__lt=timezone.now() - timedelta(days=14)
        ).delete()

        self.stdout.write(self.style.SUCCESS("Old account codes cleared!"))
