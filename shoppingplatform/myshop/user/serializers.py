from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer): #模型序列化器
    class Meta:
        model = User
        # fields = ["id","email"]
        exclude = ["password"]

class UserCreateSerializer(serializers.Serializer):
    company = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200,
        error_messages={
            'invalid':'error email',
            'null':'email not allow null',
            'blank':'nothing in here',
            'max_length':"too long"
        }
    )
    password = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    first_name = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    last_name = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    phone = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    store_credit = serializers.IntegerField(default=0)

    registration_ip_address = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    customer_group_id = serializers.IntegerField(default=0)
    def validate_customer_group_id(self, value):
        if value < 0:
            raise serializers.ValidationError('Credit must be a positive number.')
        return value

    notes = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )
    tax_exempt_category = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        max_length=200
    )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company = validated_data.get('company', instance.company)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.store_credit = validated_data.get('store_credit', instance.store_credit)
        instance.registration_ip_address = validated_data.get('registration_ip_address',
                                                              instance.registration_ip_address)
        instance.customer_group_id = validated_data.get('customer_group_id', instance.customer_group_id)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.tax_exempt_category = validated_data.get('tax_exempt_category', instance.tax_exempt_category)
        instance.save()
        return instance


