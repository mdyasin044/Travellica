from django.shortcuts import render
from travello.models import User, Review, ReviewImages, ReviewInstance, PopularDestination
from datetime import datetime


def get_all_locations():
    locations = []
    reviews = Review.objects.all()
    for review in reviews:
        if review.review_location not in locations:
            locations.append(review.review_location)
    return locations


def get_popular_destinations():
    locations = get_all_locations()
    destinations = []
    for location in locations:
        dest = PopularDestination()
        dest.images = []
        for ri in ReviewImages.objects.filter(review_location=location):
            dest.images.append(ri.review_image)
        dest.location = location
        dest.review_count = Review.objects.filter(review_location=location).count()
        destinations.append(dest)
    return destinations


def get_latest_reviews():
    reviews = Review.objects.all()
    reviewInstances = []
    for review in reviews:
        instance = ReviewInstance()
        instance.date = review.date
        instance.time = review.time
        instance.title = review.review_title
        instance.location = review.review_location
        instance.description = review.review_description
        instance.reviewer_name = review.reviewer_name
        instance.reviewer_image = []
        users = User.objects.filter(username=review.reviewer_name)
        for user in users:
            instance.reviewer_image.append(user.profilePhoto)
        instance.images = []
        rimages = ReviewImages.objects.filter(date=review.date, time=review.time, reviewer_name=review.reviewer_name)
        for img in rimages:
            instance.images.append(img.review_image)
        reviewInstances.append(instance)
    reviewInstances.reverse()
    return reviewInstances


def common_post_method_handler(request):
    if request.method == 'POST':
        if 'id_input_profilephoto' in request.FILES and 'id_input_biodata' in request.POST and 'id_input_username' in request.POST and 'id_input_email' in request.POST and 'id_input_password' in request.POST:
            profilePhoto = request.FILES['id_input_profilephoto']
            bioData = request.POST['id_input_biodata']
            username = request.POST['id_input_username']
            email = request.POST['id_input_email']
            password = request.POST['id_input_password']
            userModel = User(profilePhoto=profilePhoto, bioData=bioData, username=username, email=email, password=password)
            userModel.save()
            print(bioData)
            print(username)
            print(email)
            print(password)
            request.session['currentUser'] = username
            return True

        if 'id_input_title' in request.POST and 'id_input_location' in request.POST and 'id_textarea_description' in request.POST:
            date_data = datetime.now().date().strftime("%B %d, %Y")
            time_data = datetime.now().time().strftime("%H:%M:%S")
            reviewer_name = request.session.get('currentUser', '')
            reviewer_email = ''
            review_title = request.POST['id_input_title']
            review_location = request.POST['id_input_location']
            review_description = request.POST['id_textarea_description']
            reviewModel = Review(date=date_data, time=time_data, reviewer_name=reviewer_name, reviewer_email=reviewer_email,
                                 review_title=review_title, review_location=review_location, review_description = review_description)
            reviewModel.save()
            for review_image in request.FILES.getlist("id_input_images"):
                reviewImagesModel = ReviewImages(date=date_data, time=time_data, reviewer_name=reviewer_name,
                                                 reviewer_email=reviewer_email, review_location=review_location,
                                                 review_image=review_image)
                reviewImagesModel.save()
            print(date_data)
            print(time_data)
            print(reviewer_name)
            print(reviewer_email)
            print(review_title)
            print(review_location)
            print(review_description)
            print(request.FILES.getlist("id_input_images"))
            return True

        if 'id_input_loginid' in request.POST and 'id_input_loginpass' in request.POST:
            username = request.POST['id_input_loginid']
            password = request.POST['id_input_loginpass']
            users = User.objects.filter(username=username, password=password)
            if users.count() == 1:
                request.session['currentUser'] = username
                return True

    return False


def common_get_method_handler(request):
    if request.method == 'GET':
        if request.GET.get('signin_status', '') == 'false':
            request.session['currentUser'] = ''


def index(request):
    common_post_method_handler(request)
    common_get_method_handler(request)
    return render(request, "index.html", {
        'destinations': get_popular_destinations(),
        'latest_reviews': get_latest_reviews(),
        'currentUser': request.session.get('currentUser', '')
    })


def destination(request):
    common_post_method_handler(request)
    common_get_method_handler(request)
    if request.method == 'GET' and request.GET.get('dest', '') != '':
        dest = request.GET.get('dest')
        reviews = Review.objects.filter(review_location=dest)
        reviewInstances = []
        for review in reviews:
            instance = ReviewInstance()
            instance.date = review.date
            instance.title = review.review_title
            instance.location = review.review_location
            instance.description = review.review_description
            instance.reviewer_name = review.reviewer_name
            instance.reviewer_image = []
            users = User.objects.filter(username=review.reviewer_name)
            for user in users:
                instance.reviewer_image.append(user.profilePhoto)
            instance.images = []
            rimages = ReviewImages.objects.filter(date=review.date, time=review.time, reviewer_name=review.reviewer_name)
            for img in rimages:
                instance.images.append(img.review_image)
            reviewInstances.append(instance)

    return render(request, "destination.html", {
        'destinations': reviewInstances,
        'currentUser': request.session.get('currentUser', '')
    })


def profile(request):
    common_post_method_handler(request)
    common_get_method_handler(request)
    if request.method == 'GET' and request.GET.get('username', '') != '':
        username = request.GET.get('username')
        searchuser = User.objects.filter(username=username)
        reviews = Review.objects.filter(reviewer_name=username)
        reviewInstances = []
        for review in reviews:
            instance = ReviewInstance()
            instance.date = review.date
            instance.title = review.review_title
            instance.location = review.review_location
            instance.description = review.review_description
            instance.images = []
            reviewImages = ReviewImages.objects.filter(date=review.date, time=review.time, reviewer_name=review.reviewer_name)
            for img in reviewImages:
                instance.images.append(img.review_image)
            reviewInstances.append(instance)

    return render(request, "profile.html", {
        'currentUser': request.session.get('currentUser', ''),
        'searchUser': searchuser[0],
        'reviewList': reviewInstances,
    })
