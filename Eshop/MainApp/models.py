from django.db import models
from django.contrib.auth.forms import User


class Product(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    basicPrice = models.IntegerField()
    discount = models.IntegerField()
    price = models.IntegerField()
    img1 = models.ImageField(upload_to='images')
    img2 = models.ImageField(upload_to='images',default=None)
    img3 = models.ImageField(upload_to='images',default=None)
    img4 = models.ImageField(upload_to='images',default=None)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    cartid=models.AutoField
    cart_user=models.ForeignKey(User,on_delete="CASCADE",default=None)
    cart_product=models.ForeignKey(Product,on_delete="CASCADE",default=None)
    count=models.IntegerField(default=1)
    total=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now_add=True)

class Checkout(models.Model):
    checkid=models.CharField(max_length=30,primary_key=True,default=None)
    checkout_user = models.ForeignKey(User, on_delete="CASCADE", default=None)
    chname=models.CharField(max_length=30)
    mobile=models.IntegerField()
    email=models.EmailField(max_length=50)
    state=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    pin=models.CharField(max_length=10)

    def __str__(self):
        return self.chname

class Order(models.Model):
    orderid =  models.AutoField
    ordernumber = models.IntegerField()
    order_user=models.ForeignKey(User,on_delete="CASCADE",default=None)
    order_product=models.ForeignKey(Product,on_delete="CASCADE",default=None)
    count=models.IntegerField(default=1)
    order_address=models.ForeignKey(Checkout,on_delete="CASCADE",default=None)

class PreviousOrder(models.Model):
    orderid =  models.AutoField
    ordernumber = models.IntegerField()
    order_user=models.ForeignKey(User,on_delete="CASCADE",default=None)
    order_product=models.ForeignKey(Product,on_delete="CASCADE",default=None)
    count=models.IntegerField(default=1)
    order_address=models.ForeignKey(Checkout,on_delete="CASCADE",default=None)