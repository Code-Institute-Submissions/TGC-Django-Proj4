from django.urls import path
import reviews.views

urlpatterns = [
    path("", reviews.views.index, name="review_home"),
]
