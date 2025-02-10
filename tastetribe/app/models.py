from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Dish(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    img=models.FileField()
    cuisine=models.TextField()
    prep=models.IntegerField()
    cook=models.IntegerField()
    likes=models.IntegerField()

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)

class Ratings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    ratings=models.TextField()


class Ingredients(models.Model):
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    item=models.TextField()

class Cooking(models.Model):
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    steps=models.TextField()

class Bio(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.FileField()
    bio=models.TextField()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Ensure that a user can't follow the same user more than once

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

