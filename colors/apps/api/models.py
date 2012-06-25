from django.db import models

class UploadFiles(models.Model):
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

