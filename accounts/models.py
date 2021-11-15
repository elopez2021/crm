from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True) #you need to install pip install pillow and then go to settings.py to configure where is going to be stored
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    #This will return the value of name so it can be shown in the admin panel, instead of CustomerObject(1)

  #null=True means that the field can be left blank

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Our Door', 'Out Door'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    #tags means that one product can have more than one relationship. Like a ball can be for summer and also it can be used for sports

    def __str__(self):
        return self.name

class Order(models.Model):
    #we want to able to change from drop-down menu, and these are gonna be tuples 
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)

    #on_delete= models.SET_NULL is gonna do is anytime we remove this orders customer, this order will remain in the database just with a no value for customer. 

    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=100, null=True)

    #ADD CHOICES. Anytime we're actually creating a new order will have a drop-down menu and  we're gonna be able to select one of these

    def __str__(self):
        return self.product.name
        #product.name because it will go to product and select the product name