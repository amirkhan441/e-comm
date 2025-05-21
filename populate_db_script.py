import os
import django
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

# Import models after setting up Django
from store.models import Category, Product
from store.fixtures.products import men_products, women_products, unisex_products, categories

def populate_db():
    print('Populating database...')
    
    # Delete existing data
    Category.objects.all().delete()
    Product.objects.all().delete()
    
    # Create categories
    created_categories = {}
    for category_data in categories:
        category = Category.objects.create(
            name=category_data['name'],
            slug=category_data['slug']
        )
        created_categories[category_data['slug']] = category
        print(f'Created category: {category.name}')
    
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
        
        print(f'Created product: {product.name} - {product.gender.title()} - {product.collection.title()} - {category.name}')
    
    print(f'Done! Added {len(all_products)} products.')

if __name__ == "__main__":
    populate_db() 