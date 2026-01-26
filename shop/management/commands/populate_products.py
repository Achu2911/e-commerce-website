from django.core.management.base import BaseCommand
from shop.models import Category, Product
import requests
import os
from django.conf import settings
from django.core.files import File
from io import BytesIO


class Command(BaseCommand):
    help = 'Populate database with hair care categories and products'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories and products...')

        # Create categories
        hair_oil_category, created = Category.objects.get_or_create(
            name='Hair Oil',
            defaults={
                'slug': 'hair-oil',
                'description': 'Natural and herbal hair oils for healthy hair growth'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {hair_oil_category.name}'))
        else:
            self.stdout.write(f'Category already exists: {hair_oil_category.name}')

        hair_shampoo_category, created = Category.objects.get_or_create(
            name='Hair Shampoo',
            defaults={
                'slug': 'hair-shampoo',
                'description': 'Premium hair shampoos for different hair concerns'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {hair_shampoo_category.name}'))
        else:
            self.stdout.write(f'Category already exists: {hair_shampoo_category.name}')

        hair_accessories_category, created = Category.objects.get_or_create(
            name='Hair Accessories',
            defaults={
                'slug': 'hair-accessories',
                'description': 'Essential hair care accessories and tools'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {hair_accessories_category.name}'))
        else:
            self.stdout.write(f'Category already exists: {hair_accessories_category.name}')

        # Product data with image URLs from Unsplash (free, open source)
        products_data = [
            # Hair Oils
            {
                'name': 'Plant Based Herbal Hair Oil',
                'slug': 'plant-based-herbal-hair-oil',
                'category': hair_oil_category,
                'description': 'A nourishing blend of natural herbs and plant extracts that promotes hair growth and strengthens hair follicles. Rich in vitamins and minerals.',
                'price': 299.00,
                'discount_price': 249.00,
                'stock': 50,
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Onion Hair Oil',
                'slug': 'onion-hair-oil',
                'category': hair_oil_category,
                'description': 'Enriched with onion extract, this oil helps reduce hair fall and promotes new hair growth. Suitable for all hair types.',
                'price': 199.00,
                'discount_price': 169.00,
                'stock': 75,
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Rosemary Hair Oil',
                'slug': 'rosemary-hair-oil',
                'category': hair_oil_category,
                'description': 'Infused with rosemary essential oil, known for stimulating hair follicles and improving circulation to the scalp.',
                'price': 249.00,
                'discount_price': 199.00,
                'stock': 60,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Hibiscus Hair Oil',
                'slug': 'hibiscus-hair-oil',
                'category': hair_oil_category,
                'description': 'Made with hibiscus flowers, this oil conditions hair, prevents split ends, and adds natural shine to your locks.',
                'price': 229.00,
                'stock': 45,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Fenugreek Hair Oil',
                'slug': 'fenugreek-hair-oil',
                'category': hair_oil_category,
                'description': 'Rich in proteins and nicotinic acid, fenugreek oil helps strengthen hair roots and prevents premature graying.',
                'price': 179.00,
                'stock': 55,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            # Hair Accessories
            {
                'name': 'Neem Comb',
                'slug': 'neem-comb',
                'category': hair_accessories_category,
                'description': 'Natural neem wood comb that helps distribute scalp oils evenly, reduces static, and prevents hair breakage.',
                'price': 149.00,
                'stock': 100,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Hair Massager',
                'slug': 'hair-massager',
                'category': hair_accessories_category,
                'description': 'Ergonomic scalp massager that improves blood circulation, reduces stress, and promotes healthy hair growth.',
                'price': 299.00,
                'discount_price': 249.00,
                'stock': 80,
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Hair Scalp Serum',
                'slug': 'hair-scalp-serum',
                'category': hair_accessories_category,
                'description': 'Lightweight serum that nourishes the scalp, reduces dryness, and creates optimal conditions for hair growth.',
                'price': 399.00,
                'discount_price': 349.00,
                'stock': 65,
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Hair Anti-Frizz Serum',
                'slug': 'hair-anti-frizz-serum',
                'category': hair_accessories_category,
                'description': 'Smoothing serum that tames frizz, adds shine, and protects hair from humidity and environmental damage.',
                'price': 349.00,
                'stock': 70,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&h=800&fit=crop&q=80'
            },
            # Hair Shampoos
            {
                'name': 'Hibiscus Shampoo',
                'slug': 'hibiscus-shampoo',
                'category': hair_shampoo_category,
                'description': 'Gentle cleansing shampoo with hibiscus extract that adds shine, prevents hair fall, and promotes hair growth.',
                'price': 199.00,
                'discount_price': 169.00,
                'stock': 90,
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Anti-Hairfall Shampoo',
                'slug': 'anti-hairfall-shampoo',
                'category': hair_shampoo_category,
                'description': 'Formulated with biotin and keratin, this shampoo strengthens hair from roots and significantly reduces hair fall.',
                'price': 249.00,
                'discount_price': 219.00,
                'stock': 85,
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Dandruff Free Shampoo',
                'slug': 'dandruff-free-shampoo',
                'category': hair_shampoo_category,
                'description': 'Contains tea tree oil and zinc pyrithione to effectively treat dandruff and maintain a healthy, flake-free scalp.',
                'price': 229.00,
                'stock': 75,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&q=80'
            },
            {
                'name': 'Moisturizing Shampoo',
                'slug': 'moisturizing-shampoo',
                'category': hair_shampoo_category,
                'description': 'Deeply hydrating shampoo with argan oil and shea butter that restores moisture and leaves hair soft and manageable.',
                'price': 219.00,
                'discount_price': 189.00,
                'stock': 80,
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&q=80'
            },
        ]

        # Create products
        created_count = 0
        updated_count = 0

        for product_data in products_data:
            image_url = product_data.pop('image_url', None)
            
            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )

            # Download and set image if URL provided
            if image_url and (created or not product.image):
                try:
                    response = requests.get(image_url, timeout=10)
                    if response.status_code == 200:
                        image_name = f"{product.slug}.jpg"
                        product.image.save(
                            image_name,
                            File(BytesIO(response.content)),
                            save=True
                        )
                        self.stdout.write(f'  Downloaded image for: {product.name}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Could not download image for {product.name}: {str(e)}'))

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                updated_count += 1
                self.stdout.write(f'Updated product: {product.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully populated database!\n'
            f'Created: {created_count} products\n'
            f'Updated: {updated_count} products'
        ))

