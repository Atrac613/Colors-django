from django.db import models
from django.contrib.auth.models import User

class UserProfiles(models.Model):
    user = models.ForeignKey(User)
    secret_token = models.CharField(max_length=200)
    created_at = models.DateTimeField('date published')

class UploadFiles(models.Model):
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=100)
    page_id = models.CharField(max_length=20)
    colors = models.TextField()
    delete_flag = models.BooleanField()
    created_at = models.DateTimeField('date published')

class ImageRGB(models.Model):
    upload_file = models.ForeignKey(UploadFiles)
    red = models.SmallIntegerField()
    green = models.SmallIntegerField()
    blue = models.SmallIntegerField()

class ImageHSV(models.Model):
    upload_file = models.ForeignKey(UploadFiles)
    hue = models.SmallIntegerField()
    saturation = models.SmallIntegerField()
    value = models.SmallIntegerField()

class ColorNameJa(models.Model):
    name = models.CharField(max_length=100)
    name_yomi = models.CharField(max_length=100)
    red = models.SmallIntegerField()
    green = models.SmallIntegerField()
    blue = models.SmallIntegerField()

class ColorNameEn(models.Model):
    name = models.CharField(max_length=100)
    red = models.SmallIntegerField()
    green = models.SmallIntegerField()
    blue = models.SmallIntegerField()
