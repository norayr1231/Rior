from django.contrib import admin
from .models import Product, DesignRequest

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display  = ('slug', 'created_at')
    readonly_fields = ('slug', 'created_at', 'ai_response')
    filter_horizontal = ('products',)
