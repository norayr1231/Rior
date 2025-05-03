import json
from rest_framework.test import APITestCase
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

class ProductDetailTests(APITestCase):
    def test_product_detail_invalid_id(self):
        """
        Ensure we get an error when the product ID is invalid.
        """
        url = reverse('core:product-detail', kwargs={'pk': 'invalid'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_detail_nonexistent_id(self):
        """
        Ensure we get an error when the product does not exist.
        """
        url = reverse('core:product-detail', kwargs={'pk': 999})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=19.99
        )
        self.related_product = Product.objects.create(
            name='Related Product',
            description='Related Description',
            price=9.99
        )
        self.product.related_products.add(self.related_product)
        self.url = reverse('core:product-detail', kwargs={'pk': self.product.pk})

    def test_get_product_detail(self):
        """
        Ensure we can retrieve a product detail with related products.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
        self.assertEqual(response.data['related_products'][0]['name'], 'Related Product')

class DesignRequestCreateTests(APITestCase):
    def test_create_design_request_invalid_file_size(self):
        """
        Ensure we get an error when file size exceeds limits.
        """
        url = reverse('core:design-request-create')
        # Create a large file
        file = BytesIO()
        image = Image.new('RGB', (1000, 1000))  # Large image
        image.save(file, 'jpeg')
        file.seek(0)
        floor_plan = SimpleUploadedFile("floor_plan.jpg", file.read(), content_type="image/jpeg")
        interior_photo = SimpleUploadedFile("interior_photo.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        data = {
            'floor_plan': floor_plan,
            'interior_photo': interior_photo,
            'door_height': 2.0,
            'ceiling_height': 3.0,
            'area': 100.0,
            'wall_area': 40.0,
            'perimeter': 40.0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_design_request_invalid_file_format(self):
        """
        Ensure we get an error when file format is invalid.
        """
        url = reverse('core:design-request-create')
        floor_plan = SimpleUploadedFile("floor_plan.png", generate_dummy_image().read(), content_type="image/png")
        interior_photo = SimpleUploadedFile("interior_photo.png", generate_dummy_image().read(), content_type="image/png")
        data = {
            'floor_plan': floor_plan,
            'interior_photo': interior_photo,
            'door_height': 2.0,
            'ceiling_height': 3.0,
            'area': 100.0,
            'wall_area': 40.0,
            'perimeter': 40.0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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
            'ceiling_height': 3.0,
            'area': 100.0,
            'wall_area': 40.0,
            'perimeter': 40.0
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

    def test_create_design_request_invalid_file_type(self):
        """
        Ensure we get an error when providing invalid file types.
        """
        url = reverse('core:design-request-create')
        floor_plan = SimpleUploadedFile("floor_plan.txt", b"Invalid file content", content_type="text/plain")
        interior_photo = SimpleUploadedFile("interior_photo.txt", b"Invalid file content", content_type="text/plain")
        data = {
            'floor_plan': floor_plan,
            'interior_photo': interior_photo,
            'door_height': 2.0,
            'ceiling_height': 3.0,
            'area': 100.0,
            'wall_area': 40.0,
            'perimeter': 40.0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_design_request_missing_required_fields(self):
        """
        Ensure we get an error when missing required fields.
        """
        url = reverse('core:design-request-create')
        data = {
            'floor_plan': SimpleUploadedFile("floor_plan.jpg", generate_dummy_image().read(), content_type="image/jpeg"),
            'interior_photo': SimpleUploadedFile("interior_photo.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DesignRequestDetailTests(APITestCase):
    def test_design_request_detail_invalid_fields(self):
        """
        Ensure invalid fields in the request are handled properly.
        """
        # Add invalid field to data
        data = {'invalid_field': 'invalid_value'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def setUp(self):
        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.00)
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.00)
        self.product1.related_products.add(self.product2)
        floor_plan = SimpleUploadedFile("floor_plan.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        interior_photo = SimpleUploadedFile("interior_photo.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        self.design_request = DesignRequest.objects.create(
            floor_plan=floor_plan,
            interior_photo=interior_photo,
            door_height=2.0,
            ceiling_height=3.0,
            area=100.0,
            wall_area=40.0,
            perimeter=40.0,
            ai_response={
                'design_image': '/media/examples/sample_design.png',
                'products': [
                    {
                        'id': self.product1.id,
                        'name': 'Product 1',
                        'price': 10.00,
                        'image': '/media/images/1.jpg',
                        'similarity_score': 0.85,
                        'area': 85.5,
                        'perimeter': 46.3,
                        'wall_area': 120.0,
                        'related_products': [
                            {
                                'id': self.product2.id,
                                'name': 'Product 2',
                                'price': 20.00,
                                'image': '/media/images/2.jpg'
                            }
                        ]
                    },
                    {
                        'id': self.product2.id,
                        'name': 'Product 2',
                        'price': 20.00,
                        'image': '/media/images/2.jpg',
                        'similarity_score': 0.91,
                        'related_products': [
                            {
                                'id': self.product1.id,
                                'name': 'Product 1',
                                'price': 10.00,
                                'image': '/media/images/1.jpg'
                            }
                        ]
                    }
                ]
            }
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
        for product in response.data['products']:
            self.assertIn('related_products', product)
            self.assertTrue(isinstance(product['related_products'], list))
            if product['id'] == 1:
                self.assertEqual(len(product['related_products']), 1)
                self.assertEqual(product['related_products'][0]['name'], 'Product 2')
                self.assertEqual(str(product['related_products'][0]['price']), '20.0')
                self.assertIn('/media/images/2.jpg', product['related_products'][0]['image'])
                self.assertTrue(product['related_products'][0]['image'].endswith('.jpg'))
        self.assertEqual(response.data['door_height'], 2.0)
        self.assertEqual(response.data['ceiling_height'], 3.0)

    def test_get_design_request_invalid_id_nonexistent(self):
        """
        Ensure we get an error when the design request does not exist.
        """
        url = reverse('core:design-request-detail', kwargs={'slug': 'nonexistent-slug'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_design_request_invalid_slug_format(self):
        """
        Ensure we get an error when the slug format is invalid.
        """
        url = reverse('core:design-request-detail', kwargs={'slug': 'invalid-slug'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SlugUniquenessTests(APITestCase):
    def test_create_multiple_design_requests_unique_slugs(self):
        """
        Ensure that creating multiple design requests generates unique slugs.
        """
        url = reverse('core:design-request-create')
        floor_plan = SimpleUploadedFile("floor_plan.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        interior_photo = SimpleUploadedFile("interior_photo.jpg", generate_dummy_image().read(), content_type="image/jpeg")
        data = {
            'floor_plan': floor_plan,
            'interior_photo': interior_photo,
            'door_height': 2.0,
            'ceiling_height': 3.0,
            'area': 100.0,
            'wall_area': 40.0,
            'perimeter': 40.0
        }

        # Create first design request
        response1 = self.client.post(url, data, format='multipart')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        slug1 = response1.data['slug']

        # Create second design request with same data
        response2 = self.client.post(url, data, format='multipart')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        slug2 = response2.data['slug']

        self.assertNotEqual(slug1, slug2)