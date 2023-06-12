from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer,UserCreateSerializer
from rest_framework import status
import jwt
import time
from django.conf import settings
from myutils.bc_requests import BCCustomer

class UsersView(APIView):
    def get(self,request):
        # 查询所有用户
        users = User.objects.all()
        # 序列化器
        users_data = UserSerializer(users, many=True).data
        return Response({
            "code": 200,
            "message": "success",
            "data": {
                "list": users_data
            }
        })
    def post(self,request):
        user_data = request.data
        serializer = UserCreateSerializer(data=user_data)
        # 判断是否通过校验
        if not serializer.is_valid():
            return Response({
                "errors":serializer.errors
            })
        user = User.objects.create(
            company=user_data['company'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            store_credit=user_data['store_credit'],
            registration_ip_address=user_data['registration_ip_address'],
            customer_group_id=user_data['customer_group_id'],
            notes=user_data['notes'],
            tax_exempt_category=user_data['tax_exempt_category']
        )

        user_result = UserSerializer(user).data

        return Response({
            'code':200,
            "data":user_result
        })

class UsersDetailView(APIView):
    def get(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        user_result = UserSerializer(user).data
        return Response({
            'code':200,
            'data':user_result
        })

    def put(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        # user_data = request.data
        user_data = {
            'company': request.data.get('company', user.company),
            'email': request.data.get('email', user.email),
            'password': request.data.get('password', user.password),
            'first_name': request.data.get('first_name', user.first_name),
            'last_name': request.data.get('last_name', user.last_name),
            'phone': request.data.get('phone', user.phone),
            'store_credit': request.data.get('store_credit', user.store_credit),
            'registration_ip_address': request.data.get('registration_ip_address', user.registration_ip_address),
            'customer_group_id': request.data.get('customer_group_id', user.customer_group_id),
            'notes': request.data.get('notes', user.notes),
            'tax_exempt_category': request.data.get('tax_exempt_category', user.tax_exempt_category),
        }
        serializer = UserCreateSerializer(user,data=user_data)
        if not serializer.is_valid():
            return Response({
                "errors":serializer.errors
            })
        updated_user = serializer.save()
        user_result = UserSerializer(updated_user).data
        return Response({
            'code':200,
            'data':user_result
        })

    def delete(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({
            'code':200,
            'message':'User deleted successfully'
        })

class Login(APIView):
    authentication_classes = ()
    def post(self,request):
        login_data = request.data

        user = User.objects.filter(
            email=login_data['email'],
            password=login_data['password']
        ).first()

        if not user:
            return Response({'input error'},status=status.HTTP_404_NOT_FOUND)

        payload = {
            "email":user.email,
            "exp":int(time.time()) + 24*60*60
        }
        token=jwt.encode(payload,settings.SECRET_KEY)

        return Response({
            'token':token
        })

class CustomersView(APIView):
    # 通过bcAPI获取所有用户数据
    def get(self,request):
        bc_customer = BCCustomer()
        customer = bc_customer.get_all_customers()
        return Response({
            'code': 200,
            'data': customer
        })

    def post(self, request):
        bc_customer = BCCustomer()
        data = request.data
        password = data.get('password')
        data.pop('password')
        result = bc_customer.create_a_customer(data)
        if result:
            user = User(
                company=data.get('company'),
                email=data.get('email'),
                password=password,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone=data.get('phone'),
                store_credit=data.get('store_credit'),
                registration_ip_address=data.get('registration_ip_address'),
                customer_group_id=data.get('customer_group_id'),
                notes=data.get('notes'),
                tax_exempt_category=data.get('tax_exempt_category'),
            )
            user.save()
            return Response({
                    'code': 201,
                    'data': result
                })
        else:
            return Response({
                'code': 400,
                'message': 'Failed to create customer'
            })

class CustomersDetailView(APIView):
    # 通过bcAPI获取指定用户数据
    def get(self,request,customer_id):
        bc_customer = BCCustomer()
        customer = bc_customer.get_a_customer(customer_id)
        return Response({
            'code': 200,
            'data': customer
        })

    def delete(self,request,customer_id):
        bc_customer = BCCustomer()
        customer = bc_customer.delete_a_customer(customer_id)
        return Response({
            'code': 200,
            'message': 'Customer deleted successfully'
        })

    def put(self, request, customer_id):
        bc_customer = BCCustomer()
        data = request.data
        result = bc_customer.update_a_customer(customer_id,data)
        if result:
            return Response({
                'code': 200,
                'data': result
            })
        else:
            return Response({
                'code': 400,
                'message': 'Failed to update customer'
            })