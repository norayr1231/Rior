import uuid
import os
from django.utils.text import slugify

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
    """
    Pretend to call an AI and get back:
     - design_image: our “generated” image URL
     - products: list of {id, quantity}
    """
    return {
        'design_image': '/media/examples/sample_design.png',
        'products': [
            {
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
                        'price': 20.00,
                        'image': '/media/images/2.jpg'
                    },
                    {
                        'id': 3,
                        'name': 'Product 3',
                        'price': 30.00,
                        'image': '/media/images/3.jpg'
                    }
                ]
            },
            {
                'id': 2,
                'name': 'Product 2',
                'price': 20.00,
                'image': '/media/images/2.jpg',
                'similarity_score': 0.91,
                'related_products': [
                    {
                        'id': 1,
                        'name': 'Product 1',
                        'price': 10.00,
                        'image': '/media/images/1.jpg'
                    },
                    {
                        'id': 4,
                        'name': 'Product 4',
                        'price': 40.00,
                        'image': '/media/images/4.jpg'
                    }
                ]
            }
        ]
    }
