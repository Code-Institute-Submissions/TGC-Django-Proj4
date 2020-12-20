from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.template.loader import render_to_string
from .models import Book, Category, Genre, Tag
from .forms import BookForm
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core import serializers

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
    genre = Genre.objects.all()
    tags = Tag.objects.all()
    books = Book.objects.all()
    books_nav = Book.objects.order_by('-release_date')[:2]

    return render(request, 'books/index.template.html', {
        'genre': genre,
        'tags': tags,
        'books': books,
        'books_nav': books_nav,
    })


def create_book(request):
    if request.method == "POST":
        create_form = BookForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect(reverse("Homepage"))
        else:
            return render(request, 'books/create_book.template.html', {
                'form': create_form
            })
    else:
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


def genre_filter(request):
    genre = Genre.objects.all()
    tags = Tag.objects.all()
    books = Book.objects.all()
    books_nav = Book.objects.order_by('-release_date')[:2]

    if request.method == 'GET':
        genre = request.GET.get('text', None)
        # genre_list = Book.objects.filter(title=genre)
        genre_filter = Genre.objects.values_list('id', flat=True).get(title=genre)
        data = Book.objects.filter(genre=genre_filter)
        # filtered_books = []
        # for book in data:
        #     filtered_books.append({"id": book.id, "title": book.title,
        #                            "ISBN": book.ISBN, "category": book.category.title,
        #                            "release_date": book.release_date, "price": book.price,
        #                            "reviews": book.reviews, "cover": book.cover})
        # print(genre)
        print(genre_filter)
        print(data)
        html = render_to_string('books/filtered_data.template.html', {
            "data": data
        })
        return HttpResponse(html)
        # data_json = serializers.serialize("json", Book.objects.filter(genre=genre_filter))
        # return HttpResponse(data_json)
        
    # if request.method == "GET":
    #     books_list = Book.objects.value()
    #     # books_list2 = Book.objects.value()
    #     # print(books_list2)
    #     books_json = [book for book in books_list]
    #     print(books_json)
    #     # for book in books_list:
    #     #     print(book)
    #     #     # books_json.append(list(book.value()))
    # return JsonResponse(books_json, safe=False)
