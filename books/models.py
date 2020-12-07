from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Book(models.Model):
    title = models.CharField(blank=False, max_length=255)
    ISBN = models.CharField(blank=False, max_length=50)
    publisher = models.CharField(blank=False, max_length=100)
    release_date = models.PositiveIntegerField(
        default=current_year(),
        validators=[MinValueValidator(1900),
                    max_value_current_year], blank=False)
    price = models.IntegerField(blank=False)
    reviews = models.IntegerField(blank=False)
    cover = CloudinaryField()
    desc = models.TextField(blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(blank=False, max_length=100)
    publisher = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.title