from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class PizzaCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)

class Pizza(BaseModel):
    objects = models.Manager() 
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(PizzaCategory, on_delete=models.CASCADE, related_name='pizzas')
    price=models.IntegerField()
    image = models.ImageField(upload_to="")


class Cart(BaseModel):
    objects = models.Manager() 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid=models.BooleanField(default=False)

class CartItems(BaseModel):
    objects = models.Manager() 
    Pizza=models.ForeignKey(Pizza,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')