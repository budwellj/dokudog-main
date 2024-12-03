# main_app/management/commands/seed_themes.py

from django.core.management.base import BaseCommand
from api.models import Theme

class Command(BaseCommand):
    help = 'Seed themes into the database'

    def handle(self, *args, **options):
        themes = ['Sci-fi', 'Art', 'Science', 'History', 'Sports','Romance']
        for theme_name in themes:
            Theme.objects.get_or_create(name=theme_name)
        self.stdout.write(self.style.SUCCESS('Successfully seeded themes.'))
