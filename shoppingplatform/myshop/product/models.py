from django.db import models
from django.core.validators import MinValueValidator
from myutils.basemodel import BaseModel

class Product(BaseModel):
    product_name = models.CharField(null=False,blank=False,max_length=200)
    sku = models.CharField(null=False,blank=False,max_length=200)
    PHYSICAL = 'PHYSICAL'
    DIGITAL = 'DIGITAL'
    PRODUCT_TYPE_CHOICES = [
        (PHYSICAL, 'Physical'),
        (DIGITAL, 'Digital'),
    ]
    product_type = models.CharField(null=False, blank=False,max_length=8,choices=PRODUCT_TYPE_CHOICES,default=PHYSICAL,)
    default_price = models.DecimalField(max_digits=10, decimal_places=2, default=35, validators=[MinValueValidator(0)])
    brand = models.CharField(null=False,blank=False,max_length=200)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    categories = models.CharField(null=False,blank=False,max_length=200)
    description = models.CharField(null=False,blank=False,max_length=200)
    inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'product'
