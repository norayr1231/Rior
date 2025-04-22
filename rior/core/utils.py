import uuid
import os
from django.utils.text import slugify

def generate_slug():
    # e.g. “a3f1b8c2” short hex
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
    # a toy example; in reality you'd call your AI here
    return {
        'design_image': '/media/examples/sample_design.png',
        'products': [
            {'id': 1, 'quantity': 4},
            {'id': 3, 'quantity': 2},
        ]
    }
