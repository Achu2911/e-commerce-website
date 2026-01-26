import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.text import slugify

from shop.models import Product, Category, SubCategory
import difflib
import re
from django.conf import settings


def normalize(s):
    if not s:
        return ''
    return slugify(s).lower()


class Command(BaseCommand):
    help = 'Import image files from a local folder and attach them to matching models (Product/Category/SubCategory).'

    def add_arguments(self, parser):
        parser.add_argument('source', type=str, help='Source folder containing image files')
        parser.add_argument('--dry-run', action='store_true', dest='dry_run', help='Show what would be done without making changes')
        parser.add_argument('--dest-subdir', type=str, default='products', help='Destination subdirectory under MEDIA_ROOT (default: products)')

    def handle(self, *args, **options):
        src = options['source']
        dry = options['dry_run']
        dest_subdir = options['dest_subdir'].strip('/')

        if not os.path.isdir(src):
            self.stderr.write(f'Source folder not found: {src}')
            return

        # Build index of target objects by normalized keys
        prod_map = {normalize(getattr(p, 'slug', None) or p.name): p for p in Product.objects.all()}
        cat_map = {normalize(getattr(c, 'slug', None) or c.name): c for c in Category.objects.all()}
        sub_map = {normalize(getattr(s, 'slug', None) or s.name): s for s in SubCategory.objects.all()}

        files = []
        for root, dirs, filenames in os.walk(src):
            for fn in filenames:
                if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    files.append(os.path.join(root, fn))

        if not files:
            self.stdout.write('No image files found in source folder.')
            return

        matched = 0
        skipped = 0

        for fpath in files:
            fname = os.path.basename(fpath)
            name_only, ext = os.path.splitext(fname)
            key = normalize(name_only)

            target = None
            target_field = None

            # Exact slug/name match priority
            if key in prod_map:
                target = prod_map[key]
                target_field = 'image'
            elif key in cat_map:
                target = cat_map[key]
                target_field = 'image'
            elif key in sub_map:
                target = sub_map[key]
                target_field = 'image'
            else:
                # Partial containment match
                for k, p in prod_map.items():
                    if k in key or key in k:
                        target = p
                        target_field = 'image'
                        break
                # token overlap scoring
                if not target:
                    def tokens(s):
                        return set(re.split(r'[-_\s]+', s))

                    key_tokens = tokens(key)

                    best = (None, 0, None)  # (obj, score, kind)

                    for k, p in prod_map.items():
                        score = len(key_tokens & tokens(k))
                        if score > best[1]:
                            best = (p, score, 'product')

                    for k, c in cat_map.items():
                        score = len(key_tokens & tokens(k))
                        if score > best[1]:
                            best = (c, score, 'category')

                    for k, s in sub_map.items():
                        score = len(key_tokens & tokens(k))
                        if score > best[1]:
                            best = (s, score, 'subcategory')

                    if best[0] and best[1] >= 1:
                        target, _, _ = best
                        target_field = 'image'

                # Fuzzy name matching as last resort
                if not target:
                    all_keys = list(prod_map.keys()) + list(cat_map.keys()) + list(sub_map.keys())
                    close = difflib.get_close_matches(key, all_keys, n=1, cutoff=0.6)
                    if close:
                        ck = close[0]
                        if ck in prod_map:
                            target = prod_map[ck]
                            target_field = 'image'
                        elif ck in cat_map:
                            target = cat_map[ck]
                            target_field = 'image'
                        elif ck in sub_map:
                            target = sub_map[ck]
                            target_field = 'image'

            if not target:
                self.stdout.write(self.style.WARNING(f'No matching model for file: {fname}'))
                skipped += 1
                continue

            dest_name = os.path.join(dest_subdir, os.path.basename(fpath))
            rel_dest = dest_name.replace('\\', '/')

            if dry:
                self.stdout.write(f'[DRY] Would attach {fname} -> {target.__class__.__name__} id={target.pk} field={target_field} as {rel_dest}')
                matched += 1
                continue

            try:
                with open(fpath, 'rb') as fh:
                    django_file = File(fh)
                    field = getattr(target, target_field)
                    field.save(os.path.basename(rel_dest), django_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'Attached {fname} -> {target.__class__.__name__} id={target.pk}'))
                    matched += 1
            except Exception as e:
                self.stderr.write(f'Error attaching {fname}: {e}')

        self.stdout.write(self.style.NOTICE(f'Done. Matched: {matched}, Skipped: {skipped}'))
