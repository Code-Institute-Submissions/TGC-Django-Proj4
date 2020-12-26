from django.urls import path
from .views import remove_comment

urlpatterns = [
    path("del_comment/<username>/<book_id>", remove_comment, name="remove_comment"),
]
