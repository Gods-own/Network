from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    userImage = models.URLField(max_length=600, default="https://png.pngtree.com/png-clipart/20210917/ourlarge/pngtree-exquisite-webpage-with-avatar-user-placeholder-png-image_3910111.jpg")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "userImage": self.userImage
        }
        

class Posts(models.Model):
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poster")
    post = models.TextField()
    picture = models.URLField(max_length=600, blank=True, null=True)
    like = models.IntegerField(default=0)
    nocomments = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "post": self.post,
            "picture": self.picture,
            "like": self.like,
            "timestamp": self.timestamp.strftime("%b %d, %Y, %I:%M %p")
        }


# Model to check if a post has been liked by a particular student 
class Liked(models.Model):
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="postelike")
    pose = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="poses")
    liked = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "liker": self.liker.username,
            "pose": self.pose.post,
            "liked": self.liked
        }


class Comments(models.Model):
    posting = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="thepost")
    person =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commenter")
    comment = models.TextField()
    times = models.DateTimeField(auto_now_add=True)


# Model to check if a user is already following a particular user. curuser is the logged in user, followee is the user they are following    
class Following(models.Model):
    followee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    curuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    follo = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "followee": self.followee.username,
            "curuser": self.curuser.username,
            "follo": self.follo
        }


# Model to check the number of followers a user has and the number of users they are following
class NoFollows(models.Model):
    fuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fuser")
    nofollowing = models.IntegerField(default=0)
    nofollowers = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "fuser": self.fuser.username,
            "nofollowing": self.nofollowing,
            "nofollowers": self.nofollowers
        }


