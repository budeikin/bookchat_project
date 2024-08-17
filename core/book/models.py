import datetime
from time import timezone

from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField()
    date_of_death = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='authors/')
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    cover = models.ImageField(upload_to='book_covers/')
    slug = models.SlugField()

    def __str__(self):
        return self.name
