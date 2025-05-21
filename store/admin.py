from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Wishlist, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'gender', 'collection', 'in_stock', 'is_featured']
    list_filter = ['category', 'gender', 'collection', 'in_stock', 'is_featured', 'created']
    list_editable = ['price', 'in_stock', 'is_featured']
    search_fields = ['name', 'description']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'size', 'added_at']
    list_filter = ['added_at', 'size']
    search_fields = ['product__name']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    filter_horizontal = ['products']
    search_fields = ['user__username']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'country']
    search_fields = ['user__username', 'phone', 'city', 'country']
