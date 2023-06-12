from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from .models import Cart
from product.models import Product
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartCreateSerializer,CartSerializer

class CartsView(APIView):
    def get(self,request):
        # 查询所有用户
        users = User.objects.all()
        # 序列化器
        cart_items = []
        #循环
        for user in users:
            carts = Cart.objects.filter(user = user)
            if not carts.exists():
                cart_items.append({
                    'user_email': user.email,
                    "message": "The user has no products in the cart"
                })
            else:
                cart_items_user = []
                total_price = 0
                for cart in carts:
                    try:
                        product = Product.objects.get(id=cart.product.id)
                    except Product.DoesNotExist:
                        return Response({}, status=status.HTTP_404_NOT_FOUND)
                    price = cart.quantity * product.default_price
                    cart_items_user.append({
                        "cart_id":cart.id,
                        "product_name":product.product_name,
                        "default_price":product.default_price,
                        "quantity":cart.quantity,
                        "checkout":cart.checkout,
                        "price":price,
                    })
                    total_price += price
                cart_items.append({
                    'user_email': user.email,
                    "message": "success",
                    'cart_items':cart_items_user,
                    "total_price":total_price
                })
        return Response({
            "code": 200,
            "data": {
                "list": cart_items
            }
        })

class CartsAddView(APIView):
    def post(self,request,user_id,product_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({},status=status.HTTP_404_NOT_FOUND)

        quantity = request.data['quantity']
        if int(quantity) > product.inventory:
            return Response({
                'code': 400,
                'message': f"The quantity exceeds the product inventory ({product.inventory})"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_items = Cart.objects.get(user=user, product=product)
            cart_items.quantity += int(quantity)
            cart_items.save()
        except Cart.DoesNotExist:
            cart_items = Cart(user=user, product=product, quantity=quantity)
            cart_items.save()
        data_dict = {
            'cart_id': cart_items.id,
            'user_email': user.email,
            'product_name': cart_items.product.product_name,
            'quantity': cart_items.quantity,
        }
        return Response({
            'code': 200,
            'data': data_dict
            })

class CartsDetailView(APIView):
    def get(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        cart_items=[]
        total_price = 0
        carts = Cart.objects.filter(user=user)
        if not carts.exists():
            cart_items.append({
                'user_email': user.email,
                "message": "The user has no products in the cart"
            })
        else:
            cart_items_user = []
            for cart in carts:
                try:
                    product = Product.objects.get(id=cart.product.id)
                except Product.DoesNotExist:
                    return Response({}, status=status.HTTP_404_NOT_FOUND)
                price = cart.quantity * product.default_price
                cart_items_user.append({
                    "cart_id": cart.id,
                    "product_name": product.product_name,
                    "default_price": product.default_price,
                    "quantity": cart.quantity,
                    "checkout": cart.checkout,
                    "price":price
                })
                total_price += price
            cart_items.append({
                'user_email': user.email,
                "message": "success",
                'cart_items': cart_items_user,
                "total_price": total_price
            })
        return Response({
            'code': 200,
            'data': cart_items
        })

    def put(self, request, user_id):
        try:
            # 获取指定用户的购物车项
            cart = Cart.objects.get(user_id=user_id, product_id=request.data.get('product_id'))
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        cart_data = {
            'quantity': request.data.get('quantity', cart.quantity),
            'checkout': request.data.get('checkout', cart.checkout),
        }
        serializer = CartCreateSerializer(cart, data=cart_data)
        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors
            })
        updated_cart = serializer.save()
        cart_result = CartSerializer(updated_cart).data
        return Response({
            'code': 200,
            'data': cart_result
        })

class CartsDeleteView(APIView):
    def delete(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({
            'code': 200,
            'message': 'Cart deleted successfully'
        })

