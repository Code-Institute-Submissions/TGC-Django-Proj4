from django.urls import path
import books.views

urlpatterns = [
    path("", books.views.index, name="view_books_route"),
]
