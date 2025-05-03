import uuid
import os
from django.utils.text import slugify

def get_product_ids_from_ai_output(ai_output):
    """Get all product IDs including related products from AI output."""
    product_ids = set()
    for product in ai_output.get('products', []):
        product_ids.add(product.get('id'))
        for related_product in product.get('related_products', []):
            product_ids.add(related_product.get('id'))
    return list(product_ids)

def generate_slug():
    return uuid.uuid4().hex[:8]

def image_upload_path(instance, filename):
    """
    Distribute files into 100 buckets by first byte of a uuid.
    """
    ext = os.path.splitext(filename)[1]
    uid = uuid.uuid4().hex
    bucket = int(uid[:2], 16) % 100
    return f'images/{bucket}/{uid}{ext}'

def mock_ai_process(floor_plan_path, door_h, ceil_h, interior_img_path):

    return {
        'design_image': '/media/examples/sample_design.png',
        'area': 85.5,
        'perimeter': 46.3,
        'products': [
            {
                'id': 1,
                'id': 1,
                'name': 'Product 1',
                'price': 10.00,
                'image': '/media/images/1.jpg',
                'similarity_score': 0.85,
                'area': 85.5,
                'perimeter': 46.3,
                'wall_area': 120.0,
                'id': 1,                
                'name': 'Product 1',
                'price': 10.00,
                'image': '/media/images/1.jpg',
                'similarity_score': 0.85,
                'area': 85.5,
                'perimeter': 46.3,
                'wall_area': 120.0,
                'related_products': [
                    {
                        'id': 2,
                        'name': 'Product 2',
                        'store': 'Domus',
                        'price': 20.00,
                        'image': '/media/images/2.jpg'
                    },
                    {
                        'id': 3,
                        'name': 'Product 3',
                        'store': 'Domus',
                        'price': 30.00,
                        'image': '/media/images/3.jpg'
                    }
                ]
            },
            {
                'id': 2,
                'related_products': [
                    {
                        'id': 1,
                        'name': 'Product 1',
                        'store': 'Domus',
                        'price': 10.00,
                        'image': '/media/images/1.jpg'
                    },
                    {
                        'id': 3,
                        'name': 'Product 4',
                        'store': 'Domus',
                        'price': 40.00,
                        'image': '/media/images/4.jpg'
                    }
                ]
            }
        ]
    }
