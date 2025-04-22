import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Product, DesignRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

def generate_dummy_image():
    file = BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(file, 'jpeg')
    file.seek(0)
    return file


class ProductListTests(APITestCase):
    def test_get_product_list(self):
        """
        Ensure we can get list of products.
        """
        Product.objects.create(name='Product 1', description='Description 1', price=10.00)
        Product.objects.create(name='Product 2', description='Description 2', price=20.00)
        url = reverse('core:product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class DesignRequestCreateTests(APITestCase):
    def test_create_design_request_valid_input(self):
        """
        Ensure we can create a new design request.
        """
        url = reverse('core:design-request-create')
        floor_plan = SimpleUploadedFile("floor_plan.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        interior_photo = SimpleUploadedFile("interior_photo.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        data = {
            'floor_plan': floor_plan,
            'interior_photo': interior_photo,
            'door_height': 2.0,
            'ceiling_height': 3.0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DesignRequest.objects.count(), 1)
        self.assertIn('slug', response.data)

    def test_create_design_request_invalid_input(self):
        """
        Ensure we get an error when providing invalid input.
        """
        url = reverse('core:design-request-create')
        data = {}  # Missing required fields
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DesignRequestDetailTests(APITestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.00)
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.00)
        floor_plan = SimpleUploadedFile("floor_plan.jpg", b"file_content", content_type="image/jpeg")
        interior_photo = SimpleUploadedFile("interior_photo.jpg", b"file_content", content_type="image/jpeg")
        self.design_request = DesignRequest.objects.create(
            floor_plan=floor_plan,
            interior_photo=interior_photo,
            door_height=2.0,
            ceiling_height=3.0,
        )
        self.design_request.products.set([self.product1, self.product2])
        self.design_request.save()
        self.url = reverse('core:design-request-detail', kwargs={'slug': self.design_request.slug})

    def test_get_design_request_detail(self):
        """
        Ensure we can retrieve a design request detail.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], str(self.design_request.slug))
        self.assertEqual(len(response.data['products']), 2)

    def test_get_design_request_invalid_id_nonexistent(self):
        """
        Ensure we get an error when the design request does not exist.
        """
        url = reverse('core:design-request-detail', kwargs={'slug': 'nonexistent-slug'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)