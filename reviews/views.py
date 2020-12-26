from django.shortcuts import (
    render,
    HttpResponse,
    redirect,
    get_object_or_404
)
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Review
from books.models import Book

# Create your views here.


def index(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/reviews_index.template.html', {
        'reviews': reviews
    })


def remove_comment(request, username, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.user.is_superuser:
        current_user = User.objects.get(username=username).pk
        review_to_delete = Review.objects.filter(
            user=current_user, book=book_id)
        review_to_delete.delete()
        messages.error(
            request, f"Review has been deleted by {request.user.username}"
            f" on {book.title}")
        return redirect("book_info", book_id=book_id)
    elif request.user.username == username:
        current_user = request.user.id
        review_to_delete = Review.objects.filter(
            user=current_user, book=book_id)
        review_to_delete.delete()
        messages.error(
            request, f"Review has been deleted by {request.user.username}"
            f"on {book.title}")
        return redirect("book_info", book_id=book_id)
    else:
        messages.error(request, "You are not the owner of this comment")
        return redirect("book_info", book_id=book_id)
    return redirect("book_info", book_id=book_id)
