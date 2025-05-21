from django.core.management.base import BaseCommand
from store.models import Category, Product
from store.fixtures.products import adjectives, colors, description_templates

import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add winter collection products to the database'

    def handle(self, *args, **options):
        self.stdout.write('Adding winter collection products...')
        
        # Get categories or create if they don't exist
        categories = {
            'Sweaters': Category.objects.get_or_create(name='Sweaters', slug='sweaters')[0],
            'Jackets': Category.objects.get_or_create(name='Jackets', slug='jackets')[0],
            'Accessories': Category.objects.get_or_create(name='Accessories', slug='accessories')[0],
        }
        
        # Winter products for men
        men_winter_products = [
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Wool Coat',
                'description': random.choice(description_templates).format('wool coat'),
                'price': Decimal(random.randint(8999, 19999)) / 100,
                'gender': 'men',
                'collection': 'winter',
                'category': categories['Jackets'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Puffer Jacket',
                'description': random.choice(description_templates).format('puffer jacket'),
                'price': Decimal(random.randint(5999, 12999)) / 100,
                'gender': 'men',
                'collection': 'winter',
                'category': categories['Jackets'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Turtleneck Sweater',
                'description': random.choice(description_templates).format('turtleneck sweater'),
                'price': Decimal(random.randint(3999, 7999)) / 100,
                'gender': 'men',
                'collection': 'winter',
                'category': categories['Sweaters'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Wool Beanie',
                'description': random.choice(description_templates).format('wool beanie'),
                'price': Decimal(random.randint(1499, 2999)) / 100,
                'gender': 'men',
                'collection': 'winter',
                'category': categories['Accessories'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Winter Scarf',
                'description': random.choice(description_templates).format('winter scarf'),
                'price': Decimal(random.randint(1999, 3999)) / 100,
                'gender': 'men',
                'collection': 'winter',
                'category': categories['Accessories'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
        ]
        
        # Winter products for women
        women_winter_products = [
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Faux Fur Coat',
                'description': random.choice(description_templates).format('faux fur coat'),
                'price': Decimal(random.randint(8999, 19999)) / 100,
                'gender': 'women',
                'collection': 'winter',
                'category': categories['Jackets'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Quilted Jacket',
                'description': random.choice(description_templates).format('quilted jacket'),
                'price': Decimal(random.randint(5999, 12999)) / 100,
                'gender': 'women',
                'collection': 'winter',
                'category': categories['Jackets'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Cashmere Sweater',
                'description': random.choice(description_templates).format('cashmere sweater'),
                'price': Decimal(random.randint(5999, 10999)) / 100,
                'gender': 'women',
                'collection': 'winter',
                'category': categories['Sweaters'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Knit Cardigan',
                'description': random.choice(description_templates).format('knit cardigan'),
                'price': Decimal(random.randint(3999, 7999)) / 100,
                'gender': 'women',
                'collection': 'winter',
                'category': categories['Sweaters'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Winter Hat',
                'description': random.choice(description_templates).format('winter hat'),
                'price': Decimal(random.randint(1499, 2999)) / 100,
                'gender': 'women',
                'collection': 'winter',
                'category': categories['Accessories'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
        ]
        
        # Winter products for unisex
        unisex_winter_products = [
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Fleece Jacket',
                'description': random.choice(description_templates).format('fleece jacket'),
                'price': Decimal(random.randint(4999, 8999)) / 100,
                'gender': 'unisex',
                'collection': 'winter',
                'category': categories['Jackets'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
            {
                'name': f'{random.choice(adjectives)} {random.choice(colors)} Gloves',
                'description': random.choice(description_templates).format('winter gloves'),
                'price': Decimal(random.randint(1999, 3999)) / 100,
                'gender': 'unisex',
                'collection': 'winter',
                'category': categories['Accessories'],
                'in_stock': True,
                'is_featured': random.choice([True, False]),
            },
        ]
        
        # Combine all winter products
        all_winter_products = men_winter_products + women_winter_products + unisex_winter_products
        
        # Create products in the database
        for product_data in all_winter_products:
            product = Product.objects.create(
                category=product_data['category'],
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                gender=product_data['gender'],
                collection=product_data['collection'],
                in_stock=product_data['in_stock'],
                is_featured=product_data['is_featured']
            )
            self.stdout.write(f'Created winter product: {product.name} - {product.gender.title()} - {product.category.name}')
            
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(all_winter_products)} winter collection products!')) 