from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
import os

from shop.models import Product, Category, SubCategory


class Command(BaseCommand):
    help = 'Migrate existing MEDIA files to the configured DEFAULT_FILE_STORAGE (e.g. Cloudinary).'

    def handle(self, *args, **options):
        models = [Category, SubCategory, Product]
        total = 0
        migrated = 0

        for model in models:
            qs = model.objects.all()
            for obj in qs:
                # look for common image fields
                for field_name in ['image']:
                    field = getattr(obj, field_name, None)
                    if not field:
                        continue

                    # If there's no name or it's already a remote URL, skip
                    name = field.name
                    if not name:
                        continue

                    total += 1

                    local_path = os.path.join(settings.MEDIA_ROOT, name)
                    if os.path.exists(local_path):
                        try:
                            with open(local_path, 'rb') as f:
                                django_file = File(f)
                                base_name = os.path.basename(name)
                                # Re-save the file using Django storage backend
                                field.save(base_name, django_file, save=True)
                                migrated += 1
                                self.stdout.write(self.style.SUCCESS(f'Migrated {model.__name__} id={obj.pk} field={field_name} -> {field.url}'))
                        except Exception as e:
                            self.stderr.write(f'Error migrating {local_path}: {e}')
                    else:
                        self.stdout.write(self.style.WARNING(f'Local file not found: {local_path} (skipping)'))

        self.stdout.write(self.style.NOTICE(f'Done. Found {total} files, migrated {migrated}.'))
