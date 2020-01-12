from django.db import models
from users.models import User


class CategoryDb(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductDb(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=255)
    fat = models.IntegerField()
    saturated_fat = models.IntegerField()
    sugar = models.IntegerField()
    salt = models.IntegerField()
    category = models.ForeignKey(CategoryDb, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HistoricDb(models.Model):
    product_original = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='product_original')
    product_replaceable = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='product_replaceable')
    user = models.ManyToManyField(User, related_name='user')
