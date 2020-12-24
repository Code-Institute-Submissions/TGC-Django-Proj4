from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.template.loader import render_to_string
from .models import Book, Category, Genre, Tag
from reviews.models import Review
from .forms import BookForm
from reviews.forms import ReviewForm
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


def redirect_view(request):
    response = redirect('/books/')
    return response


def homepage(request):
    books = Book.objects.all()
    books_nav = books.order_by('-release_date')[:2]
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for item in cart:
        grand_total += cart[item]['subtotal']
    return render(request, 'books/homepage.template.html', {
        'books': books,
        'books_nav': books_nav,
        'grand_total': grand_total,
    })


def index(request):
    genre = Genre.objects.all()
    tags = Tag.objects.all()
    books = Book.objects.all()
    books_nav = Book.objects.order_by('-release_date')[:2]
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for item in cart:
        grand_total += cart[item]['subtotal']

    return render(request, 'books/index.template.html', {
        'genre': genre,
        'tags': tags,
        'books': books,
        'books_nav': books_nav,
        'grand_total': grand_total,
    })


@login_required
def create_book(request):
    if request.method == "POST":
        create_form = BookForm(request.POST, request.FILES)
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
    if request.method == 'GET':
        genre = request.GET.get('text', None)
        genre_filter = Genre.objects.values_list(
            'id', flat=True).get(title=genre)
        data = Book.objects.filter(genre=genre_filter)
        print(genre_filter)
        print(data)
        html = render_to_string('books/filtered_data.template.html', {
            "data": data
        })
        return HttpResponse(html)

@login_required
def book_info(request, book_id):
    books = Book.objects.all()
    books_nav = books.order_by('-release_date')[:2]
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for item in cart:
        grand_total += cart[item]['subtotal']

    book_selected = get_object_or_404(Book, pk=book_id)
    book_form = BookForm(instance=book_selected)
    review_form = ReviewForm(request.POST)
    reviews = Review.objects.filter(book=book_id)
    
    if request.method == "POST":
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.book = book_selected
            review.save()
            return redirect(book_info, book_id=book_id)
        else:
            return '/accounts/login'
       

    return render(request, 'books/book_info.template.html', {
        "books_nav": books_nav,
        "form": book_form,
        "book": book_selected,
        "reviews": reviews,
        "review_form": review_form,
        "grand_total": grand_total,
    })
