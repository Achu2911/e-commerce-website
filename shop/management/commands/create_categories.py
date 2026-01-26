from django.core.management.base import BaseCommand
from shop.models import Category, SubCategory
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Auto-create categories and subcategories"

    def handle(self, *args, **kwargs):
        data = {
            "Hair Oil": [
                "Herbal Hair Oil",
                "Hibiscus Hair Oil",
                "Fenugreek Hair Oil",
                "Rosemary Hair Oil",
            ],
            "Shampoo": [
                "Anti-Hair Fall Shampoo",
                "Anti-Dandruff Shampoo",
                "Onion Shampoo",
                "Hibiscus Shampoo",
                "Fenugreek Shampoo",
            ],
            "Hair Accessories": [
                "Clips",
                "Clutches",
                "Scrunches",
                "Hair Massager",
                "Catch Clips",
                "Cushy Clips",
            ],
        }

        for category_name, subcategories in data.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": slugify(category_name)}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category exists: {category_name}"))

            for sub_name in subcategories:
                subcat, sub_created = SubCategory.objects.get_or_create(
                    category=category,
                    name=sub_name
                )

                if sub_created:
                    self.stdout.write(self.style.SUCCESS(f"  └─ Created subcategory: {sub_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"  └─ Subcategory exists: {sub_name}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Categories & Subcategories created successfully"))
