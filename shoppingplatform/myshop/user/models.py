from django.db import models
from django.core.validators import MinValueValidator
from myutils.basemodel import BaseModel

class User(BaseModel):
    company = models.CharField(null=False,blank=False,max_length=200)
    email = models.CharField(null=False,blank=False,max_length=200)
    password = models.CharField(null=False,blank=False, max_length=200)
    first_name = models.CharField(null=False,blank=False,max_length=200)
    last_name = models.CharField(null=False,blank=False,max_length=200)
    phone = models.CharField(null=False,blank=False,max_length=200)
    store_credit = models.IntegerField(default=0)
    registration_ip_address = models.CharField(null=False,blank=False,max_length=200)
    customer_group_id = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    notes = models.CharField(null=False,blank=False,max_length=200)
    tax_exempt_category = models.CharField(null=False,blank=False,max_length=200)

    class Meta:
        db_table = 'user'
