from django.core.management.base import BaseCommand
from store.models import Category, Product
from store.fixtures.products import categories as product_categories
from store.fixtures.products import men_products, women_products, unisex_products

class Command(BaseCommand):
    help = 'Populates the database with sample products'

    def handle(self, *args, **options):
        self.stdout.write('Populating database...')
        
        # Delete existing data
        Category.objects.all().delete()
        Product.objects.all().delete()
        
        # Create categories
        created_categories = {}
        for category_data in product_categories:
            category = Category.objects.create(
                name=category_data['name'],
                slug=category_data['slug']
            )
            created_categories[category_data['slug']] = category
            self.stdout.write(f'Created category: {category.name}')
        
        # Add all products
        all_products = men_products + women_products + unisex_products
        
        # Create products
        for product_data in all_products:
            category_slug = product_data['category']
            category = created_categories[category_slug]
            
            # Create the product
            product = Product.objects.create(
                category=category,
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                gender=product_data['gender'],
                collection=product_data.get('collection', 'summer'),
                in_stock=True,
                is_featured=product_data.get('is_featured', False)
            )
            
            self.stdout.write(f'Created product: {product.name} - {product.gender.title()} - {product.collection.title()} - {category.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Done! Added {len(all_products)} products.'))