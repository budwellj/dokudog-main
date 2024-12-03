
from django.core.management.base import BaseCommand
from api.models import Language

class Command(BaseCommand):
    help = 'Seed languages into the database'

    def handle(self, *args, **options):
        languages = ['English', 'Japanese', 'Spanish', 'French', 'German', 'Mandarin', 'Korean']
        for language_name in languages:
            Language.objects.get_or_create(name=language_name)
        self.stdout.write(self.style.SUCCESS('Successfully seeded languages.'))