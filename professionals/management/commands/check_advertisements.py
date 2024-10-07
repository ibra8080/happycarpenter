from django.core.management.base import BaseCommand
from professionals.models import Advertisement

class Command(BaseCommand):
    help = 'Check the integrity of Advertisement records'

    def handle(self, *args, **options):
        self.stdout.write("Checking Advertisement records...")
        ads = Advertisement.objects.all()
        for ad in ads:
            try:
                self.stdout.write(f"ID: {ad.id}, Title: {ad.title}, Professional: {ad.professional}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error with ad ID {ad.id}: {str(e)}"))
        self.stdout.write(self.style.SUCCESS("Check completed."))
