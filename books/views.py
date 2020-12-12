from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Book, Category
from .forms import BookForm
from django.db.models import Q
from django.http import JsonResponse

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
    return render(request, 'books/create_book.template.html', {
        'form': create_form,
    })


def get_category(request):
    if request.method == 'GET':
        category_list = Category.objects.all()
        category = []
        for cat in category_list:
            category.append({"id": cat.id, "title": cat.title,
                             "publisher": cat.publisher})
    return JsonResponse(category, safe=False)
