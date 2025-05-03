from rest_framework import serializers
from .models import Product, DesignRequest

class DesignRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignRequest
        fields = [
            'slug', 'created_at', 'area', 'perimeter',
            'wall_area', 'door_height', 'ceiling_height'
        ]

class RelatedProductSerializer(serializers.Serializer):
    id    = serializers.IntegerField()
    name  = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.CharField(max_length=200)

class ProductSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()
    store_icon = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'store_name', 'store_icon']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            design_request_slug = request.parser_context['kwargs'].get('slug')
            if design_request_slug:
                try:
                    design_request = DesignRequest.objects.get(slug=design_request_slug)
                    ai_response = design_request.ai_response
                    related_products_data = []
                    for related_product in ai_response.get('products', []):
                        if related_product['id'] == instance.id:
                            related_products = related_product.get('related_products', [])
                            for rp in related_products:
                                try:
                                    product_obj = Product.objects.get(id=rp['id'])
                                    product_data = {
                                        'id': product_obj.id,
                                        'name': product_obj.name,
                                        'price': product_obj.price,
                                        'store': product_obj.store.name,
                                        'image': product_obj.image
                                    }
                                    related_products_data.append(product_data)
                                except Product.DoesNotExist:
                                    continue
                    representation['related_products'] = related_products_data
                except DesignRequest.DoesNotExist:
                    representation['related_products'] = []
        else:
             representation['related_products'] = []
        return representation
    def get_store_name(self, obj):
        return obj.store.name if obj.store else None
    def get_store_icon(self, obj):
        return obj.store.logo if obj.store else None

class DesignRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignRequest
        fields = [
            'name',
            'floor_plan', 'interior_photo',
            'door_height', 'ceiling_height',
        ]

class DesignRequestResultSerializer(serializers.ModelSerializer):
    products         = ProductSerializer(many=True, read_only=True)
    area             = serializers.ReadOnlyField()
    perimeter        = serializers.ReadOnlyField()
    wall_area        = serializers.ReadOnlyField()
    design_image_url = serializers.SerializerMethodField()
    unique_link      = serializers.SerializerMethodField()

    class Meta:
        model = DesignRequest
        fields = [
            'name',
            'slug', 'created_at',
            'design_image_url', 'products', 'unique_link',
            'area', 'perimeter', 'wall_area', 'door_height',
            'ceiling_height'
        ]
        read_only_fields = ['area', 'perimeter', 'wall_area', 'created_at', 'slug', 'design_image_url', 'unique_link', 'door_height', 'ceiling_height']

    def get_design_image_url(self, obj):
        return obj.design_image.url if obj.design_image else None

    def get_unique_link(self, obj):
        return f"http://127.0.0.1:8000/api/design-requests/{obj.slug}"
