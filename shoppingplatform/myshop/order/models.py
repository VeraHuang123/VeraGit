from django.db import models
from myutils.basemodel import BaseModel
from user.models import User
from product.models import Product
from cart.models import Cart

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    country = models.CharField(null=False, blank=False, max_length=200)
    province = models.CharField(null=False, blank=False, max_length=200)
    city = models.CharField(null=False, blank=False, max_length=200)
    shipping_address = models.CharField(null=False, blank=False, max_length=200)
    billing_address = models.CharField( max_length=200)
    postal_code = models.CharField(null=False, blank=False, max_length=200)
    payment = models.CharField(null=False, blank=False, max_length=200)

    class Meta:
        db_table = 'order'