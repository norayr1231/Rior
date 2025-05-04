from rest_framework import serializers
from .models import DesignRequest, Product
from .serializers import DesignRequestResultSerializer
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class DesignRequestResultSerializerTests(APITestCase):
    def setUp(self):
        self.design_request = DesignRequest.objects.create()
        self.product1 = Product.objects.create(price=100, design_request=self.design_request)
        self.product2 = Product.objects.create(price=200, design_request=self.design_request)
        self.serializer = DesignRequestResultSerializer(self.design_request)

    def test_total_price_calculation(self):
        self.assertEqual(self.serializer.data['total_price'], 300)
        
    def test_read_only_total_price(self):
        try:
            self.serializer.initial_data['total_price'] = 500
            self.serializer.is_valid()
            self.serializer.save()
            self.fail("total_price should be read-only")
        except serializers.ValidationError:
            pass

    def test_empty_products(self):
        design_request = DesignRequest.objects.create()
        serializer = DesignRequestResultSerializer(design_request)
        self.assertEqual(serializer.data['total_price'], 0)

class SlugUniquenessTests(APITestCase):
    pass