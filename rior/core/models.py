from django.db import models
from django.db.models import JSONField
from .utils import generate_slug, image_upload_path


class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to=image_upload_path)

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    slug           = models.SlugField(unique=True, default=generate_slug)
    created_at     = models.DateTimeField(auto_now_add=True)
    floor_plan     = models.ImageField(upload_to=image_upload_path)
    interior_photo = models.ImageField(upload_to=image_upload_path)
    door_height    = models.FloatField()
    ceiling_height = models.FloatField()
    ai_response    = JSONField(blank=True, null=True)
    design_image   = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        null=True
    )
    products       = models.ManyToManyField('core.Product', blank=True)

    def __str__(self):
        return f"Request {self.slug}"