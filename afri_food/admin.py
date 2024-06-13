from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')

class MarketCategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName',)
    search_fields = ('categoryName',)

class MarketAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'isActive', 'isFeatured', 'completed', 'owner', 'category')
    search_fields = ('title', 'description', 'owner__username', 'category__categoryName')
    list_filter = ('isActive', 'isFeatured', 'completed', 'category')

class MarketImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image')
    search_fields = ('item__title',)

class MarketCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'item', 'message')
    search_fields = ('author__username', 'item__title', 'message')

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]
    prepopulated_fields = {"slug": ("name",)}

class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ImageInline(GenericTabularInline):
    model = Image
    extra = 1

class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1

class OilAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]

class CrayFishAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]

class CatFishAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]

class PonmoByKgAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]

class PonmoByPieceAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ('content_object', 'quantity')
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    inlines = [OrderItemInline]

# Register your models with the custom admin configurations
admin.site.register(User, UserAdmin)
admin.site.register(MarketCategory, MarketCategoryAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Oil, OilAdmin)
admin.site.register(CrayFish, CrayFishAdmin)
admin.site.register(CatFish, CatFishAdmin)
admin.site.register(PonmoByKg, PonmoByKgAdmin)
admin.site.register(PonmoByPiece, PonmoByPieceAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)