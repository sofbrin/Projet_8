from django.db import models
from django.db.models import Q

from users.models import User


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class CategoryDb(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class ProductDb(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    nutriscore = models.CharField(max_length=255)
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    category = models.ForeignKey(CategoryDb, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserPersonalDb(BaseModel):
    original_product = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='original_product')
    replaced_product = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='replaced_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['original_product', 'replaced_product', 'user'], name='no_double')
        ]
