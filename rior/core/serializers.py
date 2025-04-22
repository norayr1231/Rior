from rest_framework import serializers
from .models import Product, DesignRequest

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']

class DesignRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignRequest
        fields = [
            'floor_plan', 'interior_photo',
            'door_height', 'ceiling_height'
        ]

class DesignRequestResultSerializer(serializers.ModelSerializer):
    products         = ProductSerializer(many=True)
    design_image_url = serializers.SerializerMethodField()
    unique_link      = serializers.SerializerMethodField()

    class Meta:
        model = DesignRequest
        fields = [
            'slug', 'created_at',
            'design_image_url', 'products', 'unique_link'
        ]

    def get_design_image_url(self, obj):
        return obj.design_image.url if obj.design_image else None

    def get_unique_link(self, obj):
        # adjust domain in production
        return f"https://your-domain.com/design/{obj.slug}"
