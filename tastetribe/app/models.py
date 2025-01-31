from django.db import models

# Create your models here.

class Dish(models.Model):
    name=models.TextField()
    img=models.FileField()
    cuisine=models.TextField()
    prep=models.IntegerField()
    cook=models.IntegerField()

class Ingredients(models.Model):
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    item=models.TextField()

class Cooking(models.Model):
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    steps=models.Model()