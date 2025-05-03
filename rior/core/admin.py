from django.contrib import admin
from .models import Product, DesignRequest, Store

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display  = ('slug', 'created_at')
    readonly_fields = ('slug', 'created_at', 'ai_response')
    filter_horizontal = ('products',)