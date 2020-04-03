from django.db import models
import re

class ProductManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['title_length'] = "Name must consist of at least 3 characters"
        if len(postData['desc']) < 3:
            errors['desc_length'] = "Description must consist of at least 3 characters"
        return errors

class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    picture = models.ImageField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if user:
            errors['unique_email'] = "Email already taken"
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name_length'] = "First and/or Last Name must be two or more characters"
        if not postData['first_name'].isalpha and not postData['last_name'].isalpha:
            errors['name_char'] = "First and Last name should only contain alphabetic characters"
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be longer than eight characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Confirm password does not match password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Category(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AdminManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        admin = Admin.objects.filter(email=postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if admin:
            errors['unique_email'] = "Email already taken"
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name_length'] = "First and/or Last Name must be two or more characters"
        if not postData['first_name'].isalpha and not postData['last_name'].isalpha:
            errors['name_char'] = "First and Last name should only contain alphabetic characters"
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be longer than eight characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Confirm password does not match password"
        return errors


class Admin(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()

class Cart(model.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name=cart)
    products = models.ManyToManyField(Product,on_delete=models.CASCADE,related_name=cart)
