from django.shortcuts import render, HttpResponse, redirect
from .models import Book

# Create your views here.


def redirect_view(request):
    response = redirect('/books/')
    return response


def homepage(request):
    books = Book.objects.all()
    books_nav = books.order_by('-release_date')[:2]
    return render(request, 'books/homepage.template.html', {
        'books': books,
        'books_nav': books_nav,
    })


def index(request):
    return HttpResponse("Index Template")
