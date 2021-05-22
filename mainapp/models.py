from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from taggit.managers import TaggableManager

# Create your models here.
class Link(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    urlslug = models.CharField(max_length=15,null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

class Click(models.Model):
    linkref = ForeignKey(Link,on_delete=models.CASCADE)
    userref = ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return self.linkref.title + " , " +self.userref.username
