from django.db import models


class User(models.Model):
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    bioData = models.CharField(max_length=400)
    profilePhoto = models.ImageField(upload_to='static/profilephotos')

    def __str__(self):
        return self.username


class Review(models.Model):
    date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    reviewer_name = models.CharField(max_length=40)
    reviewer_email = models.CharField(max_length=40)
    review_title = models.CharField(max_length=40)
    review_location = models.CharField(max_length=40)
    review_description = models.CharField(max_length=2000)

    def __str__(self):
        return self.review_title


class ReviewImages(models.Model):
    date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    reviewer_name = models.CharField(max_length=40)
    reviewer_email = models.CharField(max_length=40)
    review_location = models.CharField(max_length=40)
    review_image = models.ImageField(upload_to='static/reviewimages')

    def __str__(self):
        return self.reviewer_name


class ReviewInstance:
    images = []
    date: str
    time: str
    title: str
    location: str
    description: str
    reviewer_image = []
    reviewer_name: str


class PopularDestination:
    images = []
    location: str
    review_count: int


class Contributor:
    image = []
    username: str
    biodata: str
    review_count: int