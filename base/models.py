from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200,unique=True)
    bio = models.TextField(null=True)
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
  
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='',  # Set it to an empty string to remove the help text
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    advertiser = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    price = models.IntegerField(null=True, blank=True)
    geartype = models.CharField(max_length=100, null=True, blank=True)
    motortype = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    num_rooms = models.IntegerField(null=True, blank=True)
    num_baths = models.IntegerField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"
