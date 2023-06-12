from rest_framework import serializers
from . import models
from .models import Cart
from user.models import User
from product.models import Product

class CartSerializer(serializers.ModelSerializer): #模型序列化器
    class Meta:
        model = Cart
        fields = '__all__'

class CartCreateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        default=1,
        allow_null=False,
    )
    checkout = serializers.ChoiceField(
        choices=models.Cart.CHECKOUT_TYPE_CHOICES,
        default='FALSE',
        allow_null=False,
    )

    def create(self, validated_data):
        user = self.context.get('user')
        product_id = self.context.get('product_id')

        # 创建购物车项
        try:
            cart = Cart.objects.get(user=user, product_id=product_id)
            cart.quantity += validated_data['quantity']
        except Cart.DoesNotExist:
            cart = Cart(user=user, product_id=product_id, quantity=validated_data['quantity'])

        cart.checkout = validated_data['checkout']
        cart.save()
        return cart

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.checkout = validated_data.get('checkout', instance.checkout)
        instance.save()
        return instance