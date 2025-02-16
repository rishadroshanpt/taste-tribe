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
    
    class Meta:
        unique_together = ('user', 'dish')

class Ratings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    ratings=models.TextField()

class Saved(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)

class Ingredients(models.Model):
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    item=models.TextField()

class Cooking(models.Model):
    dish=models.ForeignKey(Dish, on_delete=models.CASCADE)
    steps=models.TextField()

class Bio(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    img = models.FileField(upload_to='profile_pics/', default='profile_pics/profile.jpg')
    bio=models.TextField(default="Hi,I'm here")

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Ensure that a user can't follow the same user more than once

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"