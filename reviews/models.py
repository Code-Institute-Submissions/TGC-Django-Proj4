from django.db import models
from books.models import Book
from django.contrib.auth.models import User
# Create your models here.


class Review(models.Model):
    title = models.CharField(blank=False, max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return self.title
