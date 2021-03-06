from django.urls import path
import books.views

urlpatterns = [
    path("", books.views.homepage, name="homepage"),
    path("all/", books.views.index, name="show_books"),
    path("create/", books.views.create_book, name="create_book"),
    path("edit_book/<book_id>", books.views.edit_book, name="edit_book"),
    path("delete_book/<book_id>", books.views.delete_book, name="delete_book"),
    path("catsearch/", books.views.get_category, name="cat_search"),
    path("genre_filter/", books.views.genre_filter, name="genre_filter"),
    path("tag_filter/", books.views.tag_filter, name="tag_filter"),
    path("info/<book_id>", books.views.book_info, name="book_info")
]
