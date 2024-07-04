from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.IntegerField(null=True)
    record_date = models.DateField(null=True)
    def __str__(self):
        return f"User # {self.id}"

class Ibadat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    def __str__(self):
        return f"Ibadat # {self.id}"

class Scale(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ibadat = models.ForeignKey(Ibadat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    def __str__(self):
        return f"Scale # {self.id}"
    
class IbadatItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ibadat = models.ForeignKey(Ibadat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    point = models.IntegerField(null=True)
    score = models.IntegerField(null=True)
    date = models.DateField(null=True)
    def __str__(self):
        return f"Ibadat_item # {self.id}"