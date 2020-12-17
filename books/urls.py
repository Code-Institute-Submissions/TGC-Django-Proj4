from django.urls import path
import books.views

urlpatterns = [
    path("", books.views.homepage, name="Homepage"),
    path("all/", books.views.index, name="show_books"),
    path("create/", books.views.create_book, name="create_book"),
    path("catsearch/", books.views.get_category, name="cat_search"),
    path("genre_filter/", books.views.genre_filter, name="genre_filter"),
]
