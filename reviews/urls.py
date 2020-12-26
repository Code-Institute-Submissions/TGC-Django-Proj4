from django.urls import path
from .views import index, remove_comment

urlpatterns = [
    path("", index, name="review_home"),
    path("del_comment/<username>/<book_id>", remove_comment, name="remove_comment"),
]
