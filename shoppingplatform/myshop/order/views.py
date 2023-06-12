from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from .models import Order
from cart.models import Cart,CartItem
from product.models import Product
from .serializers import OrderSerializer,OrderCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from myutils.bc_requests import BCOrder

class OrdersAddView(APIView):
    def post(self,request,cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"Shopping cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            product = Product.objects.get(id=cart.product.id)
        except Product.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(id=cart.user.id)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        # 修改商品库存
        product.inventory -= cart.quantity
        product.save()

        # 新建订单
        order_data = request.data
        serializer = OrderCreateSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save(user=user, product=product, cart=cart)
            order_items = OrderSerializer(order).data

            # 清空购物车
            cart.delete()
        else:
            # 序列化失败，把错误信息返回
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        price = cart.quantity * product.default_price
        order_result = []
        order_result.append({
            'user_email': user.email,
            'cart_id': cart_id,
            "product_name": product.product_name,
            "default_price": product.default_price,
            "quantity": cart.quantity,
            "price":price,
            "order_items":order_items
        })
        return Response({
            'code': 200,
            "message": "Order successfully placed",
            'data': order_result
        })

class OrdersDetailView(APIView):
    def get(self,request,order_id):
        # 查询所有用户
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"This order cannot be found"}, status=status.HTTP_404_NOT_FOUND)
        # 序列化器
        order_data = OrderSerializer(order).data
        return Response({
            "code": 200,
            "message": "success",
            "data": {
                "list": order_data
            }
        })

    def delete(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"This order cannot be found"}, status=status.HTTP_404_NOT_FOUND)
        # 序列化器
        order.delete()
        return Response({
            "code": 200,
            "message": 'Order deleted successfully'
        })

class OrdersView(APIView):
    def get(self,request):
        # 查询所有用户
        order = Order.objects.all()
        # 序列化器
        order_data = OrderSerializer(order, many=True).data
        return Response({
            "code": 200,
            "message": "success",
            "data": {
                "list": order_data
            }
        })

class BCOrdersView(APIView):
    # 通过bcAPI获取所有用户数据
    def get(self,request):
        bc_order = BCOrder()
        order = bc_order.get_all_order()
        return Response({
            'code': 200,
            'data': order
        })

    def post(self, request):
        bc_order = BCOrder()
        data = request.data
        result = bc_order.create_a_order(data)
        if result:
            return Response({
                'code': 201,
                'data': result
            })
        else:
            return Response({
                'code': 400,
                'message': 'Failed to create order'
            })

class BCOrdersDetailView(APIView):
    # 通过bcAPI获取指定用户数据
    def get(self,request,order_id):
        bc_order = BCOrder()
        order = bc_order.get_a_order(order_id)
        return Response({
            'code': 200,
            'data': order
        })

    def put(self, request, order_id):
        bc_order = BCOrder()
        data = request.data
        result = bc_order.update_a_order(order_id,data)
        if result:
            return Response({
                'code': 200,
                'data': result
            })
        else:
            return Response({
                'code': 400,
                'message': 'Failed to update order'
            })


