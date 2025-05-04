from django.db import models
from django.db.models import JSONField
from .utils import generate_slug, image_upload_path

class Category(models.TextChoices):
    TOILET = 'Toilet'
    SINK = 'Sink'
    BATH = 'Bath'
    SHOWER = 'Shower'
    FAUCET_SINK = 'Faucet sink'
    FAUCET_BIDET = 'Faucet bidet'
    FAUCET_SHOWER = 'Faucet shower'
    BIDET = 'Bidet'
    URINAL = 'Urinal'
    ACCESORY = 'Accesory'
    DRAIN = 'Drain'
    TILE = 'Tile'



class Store(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(null=True, blank=True, upload_to=image_upload_path)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.CharField(max_length=50, choices=Category.choices, null=True)
    type = models.CharField(max_length=255, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=250, null=True)
    stock_code = models.CharField(max_length=100,null=True)
    url = models.URLField(blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    producing_country = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    height_cm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width_cm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    length_cm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(null=True, upload_to=image_upload_path)

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    name           = models.CharField(max_length=255)
    slug           = models.SlugField(unique=True, default=generate_slug)
    created_at     = models.DateTimeField(auto_now_add=True)
    floor_plan     = models.ImageField(upload_to=image_upload_path)
    interior_photo = models.ImageField(upload_to=image_upload_path)
    door_height    = models.FloatField()
    ceiling_height = models.FloatField()
    area           = models.FloatField(blank=True, null=True)
    wall_area      = models.FloatField(blank=True, null=True)
    perimeter      = models.FloatField(blank=True, null=True)
    ai_response    = JSONField(blank=True, null=True)
    design_image   = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        null=True
    )
    products       = models.ManyToManyField('core.Product', blank=True)

    def __str__(self):
        return f"Request {self.slug}"