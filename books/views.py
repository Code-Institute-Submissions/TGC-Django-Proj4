from django.shortcuts import render, HttpResponse, redirect
from .models import Book, Category
from .forms import BookForm

# Create your views here.


def redirect_view(request):
    response = redirect('/books/')
    return response


def homepage(request):
    books = Book.objects.all()
    print(books)
    books_nav = books.order_by('-release_date')[:2]
    return render(request, 'books/homepage.template.html', {
        'books': books,
        'books_nav': books_nav,
    })


def index(request):
    return HttpResponse("Index Template")


def create_book(request):
    create_form = BookForm
    publisher = Category.objects.all()
    print(publisher)
    return render(request, 'books/create_book.template.html', {
        'form': create_form,
        'publisher': publisher,
    })