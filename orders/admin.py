from django.contrib import admin
from .models import Category, Size, Dish, Product, Topping, Order, OrderItem

# Register your models here.

@admin.register (Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Size)

@admin.register (Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']

admin.site.register(Topping)

@admin.register (Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_category', 'size', 'price', 'slug']
    list_editable = ['price']
    list_filter = ['dish__category']

    def get_name(self, obj):
        return obj.dish.name
    get_name.short_description = 'Dish name'

    def get_category(self, obj):
        return obj.dish.category
    get_category.short_description = 'Category'

    def get_queryset(self, request):
        return super(ProductAdmin,self).get_queryset(request).select_related('dish')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'completed']
    list_filter = ['completed']
    inlines = [OrderItemInline]
