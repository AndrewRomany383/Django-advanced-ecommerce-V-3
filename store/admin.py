from django.contrib import admin
from .models import Category, Product, Attribute, AttributeValue, Inventory, StockControl, ReviewRating, ProductGallery
import admin_thumbnails

# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductGalleryInline]
    list_display = ('name', 'price', 'stock', 'category', 'is_active')
    list_editable = ('price', 'stock', 'is_active')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Inventory)
admin.site.register(StockControl)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
