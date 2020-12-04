from django.shortcuts import render, HttpResponse, redirect
from .models import Book

# Create your views here.


def redirect_view(request):
    response = redirect('/books/')
    return response


def homepage(request):
    books = Book.objects.order_by('-release_date')
    print(books)
    return render(request, 'books/homepage.template.html', {
        'books': books
    })


def index(request):
    return HttpResponse("Index Template")
