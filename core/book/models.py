import datetime
from time import timezone

from django import utils
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateTimeField(null=True)
    death_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='authors/')
    slug = models.SlugField()

    @property
    def age(self):
        if self.death_date:
            age = self.death_date.year - self.birth_date.year

        else:
            age = utils.timezone.now().year - self.birth_date.year
        return age

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    cover = models.ImageField(upload_to='book_covers/')
    slug = models.SlugField()

    def __str__(self):
        return self.name
