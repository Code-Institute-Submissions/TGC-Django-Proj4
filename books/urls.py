from django.urls import path
import books.views

urlpatterns = [
    path("", books.views.homepage, name="Homepage"),
    path("book/", books.views.index, name="show_books")
]
