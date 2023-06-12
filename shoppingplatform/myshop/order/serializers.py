from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer): #模型序列化器
    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.Serializer):
    country = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    province = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    city = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    shipping_address = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    billing_address = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    postal_code = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    payment = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
