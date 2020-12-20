from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("destination", views.destination, name="destination"),
    path("profile", views.profile, name="profile"),
    path("reviewimages", views.index, name="reviewimages"),
]
