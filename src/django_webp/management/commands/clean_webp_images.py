import shutil

from django.core.management.base import BaseCommand, CommandError

from django_webp.utils import WEBP_STATIC_ROOT

class Command(BaseCommand):
    help = 'Removes all cached webp images'


    def handle(self, *args, **options):
        try:
            shutil.rmtree(WEBP_STATIC_ROOT)
            self.stdout.write('Folder %s removed' % WEBP_STATIC_ROOT)
        except:
            raise CommandError('Folder %s was already removed' % WEBP_STATIC_ROOT)
