from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(default="profile2.png", null=True, blank=True)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    available = models.BooleanField(default=False, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=False, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)
    delivery = models.BooleanField(default=False)


    def __str__(self):
        template = '{0.id}({0.customer})'
        return template.format(self)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        item = orderitems.count()
        amount = float(sum([item.get_total for item in orderitems]))
        if item >= 5:
            total = amount - (amount*0.1)
            return total
        else:
            total = amount
            return total



    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{0.order},{0.product}'
        return template.format(self)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    district = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    complete = models.BooleanField(default=False, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{0.address}, {0.city}, {0.district}, {0.zipcode}.'
        return template.format(self)


class Production(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    prepared = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)

class DayOrder(models.Model):
    date = models.DateField(auto_now_add=False, null=False)