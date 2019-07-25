from django.db import models
import datetime
# Create your models here.
class Realtor(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __str__(self):
        return self.name
