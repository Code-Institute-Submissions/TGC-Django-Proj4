from django.urls import path
from .views import add_to_cart, view_cart, minus_from_cart, remove_from_cart

urlpatterns = [
    path("", view_cart, name="view_cart"),
    path("add/<book_id>", add_to_cart, name="add_to_cart"),
    path("minus/<book_id>", minus_from_cart, name="minus_from_cart"),
    path("remove/<book_id>", remove_from_cart, name="remove_from_cart"),
]
