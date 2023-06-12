# from django.shortcuts import render
from .models import Product
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    # authentication_classes = ()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

product_router = DefaultRouter()
product_router.register('product',ProductViewSet)
