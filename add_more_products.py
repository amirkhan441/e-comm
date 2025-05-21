import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

# Import models after setting up Django
from store.models import Category, Product
from store.fixtures.products import adjectives, colors, product_templates, description_templates, gender_collections

def add_more_products():
    print('Adding 50 more products to the database...')
    
    # Get existing categories or create if needed
    categories = {
        'tshirts': Category.objects.get_or_create(name='T-Shirts', slug='tshirts')[0],
        'shirts': Category.objects.get_or_create(name='Shirts', slug='shirts')[0],
        'jeans': Category.objects.get_or_create(name='Jeans', slug='jeans')[0],
        'dresses': Category.objects.get_or_create(name='Dresses', slug='dresses')[0],
        'jackets': Category.objects.get_or_create(name='Jackets', slug='jackets')[0],
        'sweaters': Category.objects.get_or_create(name='Sweaters', slug='sweaters')[0],
        'pants': Category.objects.get_or_create(name='Pants', slug='pants')[0],
        'skirts': Category.objects.get_or_create(name='Skirts', slug='skirts')[0],
        'accessories': Category.objects.get_or_create(name='Accessories', slug='accessories')[0],
        'shoes': Category.objects.get_or_create(name='Shoes', slug='shoes')[0],
    }
    
    # Create 50 new products
    created_count = 0
    for _ in range(50):
        # Select random gender
        gender = random.choice(['men', 'women', 'unisex'])
        
        # Select random collection
        collection = random.choice(['summer', 'winter'])
        
        # Select appropriate category based on gender and collection
        category_slug = random.choice(gender_collections[gender][collection])
        category = categories[category_slug]
        
        # Generate product name
        name_template = random.choice(product_templates[category_slug])
        adjective = random.choice(adjectives)
        color = random.choice(colors)
        
        # Format product name
        if random.random() < 0.7:  # 70% chance to include color
            name = name_template.format(f"{adjective} {color}")
        else:
            name = name_template.format(adjective)
            
        # Generate description
        desc_template = random.choice(description_templates)
        description = desc_template.format(category.name.lower()[:-1] if category.name.endswith('s') else category.name.lower())
        
        # Generate price (random between 19.99 and 199.99)
        price = Decimal(random.randint(1999, 19999)) / 100
        
        # Create product
        product = Product.objects.create(
            category=category,
            name=name,
            description=description,
            price=price,
            gender=gender,
            collection=collection,
            in_stock=True,
            is_featured=random.random() < 0.2  # 20% chance to be featured
        )
        
        created_count += 1
        print(f'Created product {created_count}/50: {product.name} - {gender.title()} - {collection.title()} - {category.name}')
    
    print('Done! Added 50 new products.')

if __name__ == "__main__":
    add_more_products() 