
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(AbstractUser):
    # change to blank=False to make required for more info
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))


class Product(models.Model):
    title = models.CharField(max_length=256, unique=True)
    slu = models.CharField(max_length=8, unique=True)
    description = models.TextField(max_length=4012)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    unique_wishers = models.IntegerField(default=0)

    def __str__(self):
        return f'ID-{self.id} {self.title} {self.price} MDL {self.description[:100]}'


class Wishlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    products = models.ManyToManyField('Product', blank=True)

    def __str__(self):
        return f'{self.title}'

