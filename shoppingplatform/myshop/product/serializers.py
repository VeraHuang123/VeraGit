from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer): #模型序列化器
    class Meta:
        model = Product
        fields = '__all__'
        #exclude = ["password"]
