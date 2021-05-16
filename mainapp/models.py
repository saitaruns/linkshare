from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Link(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    likes = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

