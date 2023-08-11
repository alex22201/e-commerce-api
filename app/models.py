from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from datetime import datetime

from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id: int = fields.IntField(pk=True, index=True)
    username: str = fields.CharField(max_length=20, null=False, unique=True)
    email: str = fields.CharField(max_length=255, null=False, unique=True)
    password: str = fields.CharField(max_length=100, null=False)
    is_verified: bool = fields.BooleanField(default=False)
    join_data: datetime = fields.DatetimeField(default=datetime.utcnow)


class Business(Model):
    id: int = fields.IntField(pk=True, index=True)
    name: str = fields.CharField(max_length=255, null=False, unique=True)
    city: str = fields.CharField(max_length=100, null=False, default='Unspecified')
    region: str = fields.CharField(max_length=100, null=False, default='Unspecified')
    description: str = fields.TextField(null=True)
    logo: str = fields.CharField(max_length=255, null=False, default='default.jpg')
    owner: int = fields.ForeignKeyField('models.User', related_name='Business')


class Product(Model):
    id: int = fields.IntField(pk=True, index=True)
    name: str = fields.CharField(max_length=255, null=False, unique=True)
    category: str = fields.CharField(max_length=255, null=False, unique=True)  # maby new model
    original_price: float = fields.DecimalField(max_digits=12, decimal_places=2)
    new_price: float = fields.DecimalField(max_digits=12, decimal_places=2)
    discount_percent: int = fields.IntField()
    offer_expiration_date: datetime = fields.DateField(default=datetime.utcnow)
    image: str = fields.CharField(max_length=255, null=False, default='productDefault.jpg')
    business: int = fields.ForeignKeyField('models.Business', related_name='Product')


user_pydantic = pydantic_model_creator(User, name='User', exclude=('is_verified',))
user_pydantic_in = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
user_pydantic_out = pydantic_model_creator(User, name='UserOut', exclude=('password',))

business_pydantic = pydantic_model_creator(Business, name='Business')
business_pydantic_in = pydantic_model_creator(Business, name='BusinessIn', exclude_readonly=True)


product_pydantic = pydantic_model_creator(Product, name='Product')
product_pydantic_in = pydantic_model_creator(Product, name='ProductIn', exclude=('discount_percent', 'id'))

