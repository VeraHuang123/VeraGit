from django.db import models
from myutils.basemodel import BaseModel
from user.models import User
from product.models import Product

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False,blank=False,default=1)
    CHECKOUT_TYPE_CHOICES = [
        ('FALSE', 'False'),
        ('TRUE', 'True'),
    ]
    checkout = models.CharField(null=False, blank=False, max_length=5, choices=CHECKOUT_TYPE_CHOICES,
                                    default="FALSE" )
    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"

    def get_total_price(self):
        return self.product.default_price * self.quantity

    class Meta:
        db_table = 'cart_item'