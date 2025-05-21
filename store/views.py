from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Avg, Q
from .models import Product, Category, Cart, CartItem, Wishlist, UserProfile, Order, OrderItem, Review
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

def test_view(request):
    """
    A simple test view to check if basic rendering works
    """
    return HttpResponse("<h1>Test Page</h1><p>If you can see this, basic view rendering is working.</p>")



def home(request):
    """
    Simplified home view with minimal code to avoid errors
    """
    try:
        # Get featured products if possible, but with error handling
        try:
            featured_products = Product.objects.filter(is_featured=True)[:4]
        except Exception as e:
            featured_products = []
            print(f"Error fetching featured products: {e}")
        
        # Get men's products if possible, but with error handling
        try:
            men_products = Product.objects.filter(gender='men')[:2]
        except Exception as e:
            men_products = []
            print(f"Error fetching men's products: {e}")
        
        # Get women's products if possible, but with error handling
        try:
            women_products = Product.objects.filter(gender='women')[:2]
        except Exception as e:
            women_products = []
            print(f"Error fetching women's products: {e}")
        
        # Get categories if possible, but with error handling
        try:
            categories = Category.objects.all()
        except Exception as e:
            categories = []
            print(f"Error fetching categories: {e}")
        
        context = {
            'featured_products': featured_products,
            'men_products': men_products,
            'women_products': women_products,
            'categories': categories,
        }
        return render(request, 'store/home.html', context)
    
    except Exception as e:
        # If anything fails, return a simple response
        print(f"Critical error in home view: {e}")
        return HttpResponse("<h1>StyleHub</h1><p>The site is experiencing technical difficulties. Please try again later.</p>")

def product_list(request):
    # Get filter parameters
    gender = request.GET.get('gender', '')
    collection = request.GET.get('collection', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort_by', '')
    
    # Start with all products
    products = Product.objects.filter(in_stock=True)
    
    # Apply gender filter
    if gender:
        products = products.filter(gender=gender)
    
    # Apply collection filter
    if collection:
        products = products.filter(collection=collection)
    
    # Apply price filters
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Apply sorting
    if sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created')
    else:  # featured
        products = products.order_by('-is_featured')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)  # Show 9 products per page
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'products': products_page,
        'categories': categories,
        'current_gender': gender,
        'current_collection': collection,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort_by,
        'page_obj': products_page,
    }
    return render(request, 'store/product_list.html', context)

def category_view(request, category):
    # Check if the category is a gender
    if category in ['men', 'women', 'unisex']:
        products = Product.objects.filter(gender=category, in_stock=True)
        category_obj = None
    else:
        # Try to get the category by slug
        category_obj = get_object_or_404(Category, slug=category)
        products = Product.objects.filter(category=category_obj, in_stock=True)
    
    # Get collection filter
    collection = request.GET.get('collection', '')
    if collection:
        products = products.filter(collection=collection)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)  # Show 9 products per page
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'category': category_obj,
        'gender': category if category in ['men', 'women', 'unisex'] else None,
        'products': products_page,
        'categories': categories,
        'current_collection': collection,
        'page_obj': products_page,
    }
    return render(request, 'store/category.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk, in_stock=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=pk)[:4]
    
    # Get user's review if they have one
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    # Calculate average rating
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'related_products': related_products,
        'user_review': user_review,
        'avg_rating': avg_rating,
        'categories': categories,
    }
    return render(request, 'store/product_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Create user profile, cart and wishlist
            UserProfile.objects.create(user=user)
            Cart.objects.create(user=user)
            Wishlist.objects.create(user=user)
            
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('store:login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def profile(request):
    categories = Category.objects.all()
    return render(request, 'store/profile.html', {'categories': categories})

@login_required
def view_cart(request):
    categories = Category.objects.all()
    
    # Get or create cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'categories': categories,
    }
    return render(request, 'store/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', 'M')
        
        # Check if item already exists in cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product, size=size)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity, size=size)
        
        messages.success(request, f'Added {product.name} to your cart!')
        return redirect('store:view_cart')
    
    return redirect('store:product_detail', pk=product.id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('store:view_cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('store:view_cart')

@login_required
def view_wishlist(request):
    categories = Category.objects.all()
    
    # Get or create wishlist for the user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_products = wishlist.products.all()
    
    context = {
        'wishlist': wishlist,
        'wishlist_products': wishlist_products,
        'categories': categories,
    }
    return render(request, 'store/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f'Added {product.name} to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
        
    return redirect('store:product_detail', pk=product.id)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, 'Item removed from wishlist!')
    
    return redirect('store:view_wishlist')

@login_required
def checkout(request):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:view_cart')
    
    if request.method == 'POST':
        # Get form data
        shipping_address = request.POST.get('shipping_address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            total_amount=cart.get_total()
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                price=item.product.price
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('store:order_confirmation', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': cart.get_total()
    }
    return render(request, 'store/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    try:
        # Get filter parameters
        status_filter = request.GET.get('status', '')
        date_filter = request.GET.get('date', '')
        price_sort = request.GET.get('price_sort', '')
        
        # Debug print
        print(f"Status filter: {status_filter}")
        print(f"Date filter: {date_filter}")
        print(f"Price sort: {price_sort}")
        
        # Base queryset
        orders = Order.objects.filter(user=request.user)
        
        # Apply status filter
        if status_filter:
            orders = orders.filter(status=status_filter)
            print(f"Filtered by status: {status_filter}")
        
        # Apply date filter
        if date_filter == 'oldest':
            orders = orders.order_by('created_at')
            print("Ordered by oldest first")
        else:
            orders = orders.order_by('-created_at')
            print("Ordered by most recent")
            
        # Apply price sorting
        if price_sort == 'low_to_high':
            orders = orders.order_by('total_amount')
            print("Sorted by price: low to high")
        elif price_sort == 'high_to_low':
            orders = orders.order_by('-total_amount')
            print("Sorted by price: high to low")
        
        # Debug print
        print(f"Number of orders: {orders.count()}")
        
        categories = Category.objects.all()
        
        context = {
            'orders': orders,
            'categories': categories,
            'current_status': status_filter,
            'current_date': date_filter,
            'current_price_sort': price_sort
        }
        return render(request, 'store/order_history.html', context)
    except Exception as e:
        print(f"Error in order_history view: {str(e)}")
        messages.error(request, f'Error loading order history: {str(e)}')
        return redirect('store:home')

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    # Check if user has already reviewed this product
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('store:product_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('store:product_detail', pk=pk)
    else:
        form = ReviewForm()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'form': form
    })

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('store:product_detail', pk=review.product.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'store/edit_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Your review has been deleted successfully!')
    return redirect('store:product_detail', pk=product_id)

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()
    
    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.all(),
    }
    return render(request, 'store/search_results.html', context)

# Static Pages
def about(request):
    """View for the About Us page"""
    return render(request, 'store/about.html', {'categories': Category.objects.all()})

def contact(request):
    """View for the Contact page"""
    return render(request, 'store/contact.html', {'categories': Category.objects.all()})

def faq(request):
    """View for the FAQs page"""
    return render(request, 'store/faq.html', {'categories': Category.objects.all()})

def shipping(request):
    """View for the Shipping Information page"""
    return render(request, 'store/shipping.html', {'categories': Category.objects.all()})

def returns(request):
    """View for the Returns page"""
    return render(request, 'store/returns.html', {'categories': Category.objects.all()})
