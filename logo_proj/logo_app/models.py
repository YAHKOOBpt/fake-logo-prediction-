
from django.db import models
from django.contrib.auth.models import User
class LogoPrediction(models.Model):
    image = models.ImageField(upload_to='logo_images/')
    result = models.CharField(max_length=10, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.result
    
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name",null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True, verbose_name="Category Image")
    

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return  url


class Product(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='Product_images/', null=True, blank=True, verbose_name="Product Image")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='catege', verbose_name="catege",null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL_1(self):
        try:
            url = self.image.url
        except:
            url = ''
        return  url
