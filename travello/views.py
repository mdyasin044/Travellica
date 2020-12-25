from django.shortcuts import render
from travello.models import User, Review, ReviewImages, ReviewInstance, PopularDestination, Contributor
from datetime import datetime

def match_instance(instance, review_list):
    for review in review_list:
        if instance.date == review.date and instance.time == review.time and instance.reviewer_name == review.reviewer_name:
            review_list.remove(review)
    return review_list

def get_all_locations():
    locations = []
    reviews = Review.objects.all()
    for review in reviews:
        if review.review_location not in locations:
            locations.append(review.review_location)
    return locations


def compare_destinations(dest):
    return dest.review_count


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
    return sorted(destinations, key=compare_destinations, reverse=True)


def compare_contributors(contributor):
    return contributor.review_count


def get_contributors():
    users = User.objects.all()
    contributors = []
    for user in users:
        contributor = Contributor()
        contributor.username = user.username
        contributor.biodata = user.bioData
        contributor.image = []
        contributor.image.append(user.profilePhoto)
        contributor.review_count = Review.objects.filter(reviewer_name=user.username).count()
        contributors.append(contributor)
    return sorted(contributors, key=compare_contributors, reverse=True)


def get_review_instances(reviews):
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
            usercount = User.objects.filter(username=username).count()
            if usercount == 0:
                userModel = User(profilePhoto=profilePhoto, bioData=bioData, username=username, email=email, password=password)
                userModel.save()
                request.session['currentUser'] = username
            return True

        if 'id_input_title' in request.POST and 'id_input_location' in request.POST and 'id_textarea_description' in request.POST:
            date_data = datetime.now().date().strftime("%B %d, %Y")
            time_data = datetime.now().time().strftime("%H:%M:%S")
            reviewer_name = request.session.get('currentUser', '')
            reviewer_email = 'Not saved'
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
        'destinations': get_popular_destinations()[:6],
        'currentUser': request.session.get('currentUser', ''),
        'latest_reviews': get_review_instances(Review.objects.all())[:4],
        'top_contributors': get_contributors(),
        'num_places': len(get_all_locations()),
        'num_reviews': len(get_review_instances(Review.objects.all())),
        'num_contributors': len(get_contributors()),
    })


def destination(request):
    common_post_method_handler(request)
    common_get_method_handler(request)
    reviewInstances = []
    if request.method == 'GET' and request.GET.get('type', '') == 'popular':
        for dest in get_popular_destinations():
            reviews = Review.objects.filter(review_location=dest.location)
            for instance in get_review_instances(reviews):
                reviewInstances.append(instance)
        latestReviews = []
    if request.method == 'GET' and request.GET.get('type', '') == 'latest':
        reviews = Review.objects.all()
        reviewInstances = get_review_instances(reviews)
        latestReviews = []
    if request.method == 'GET' and request.GET.get('dest', '') != '':
        dest = request.GET.get('dest')
        reviews = Review.objects.filter(review_location=dest)
        reviewInstances = get_review_instances(reviews)
        latestReviews = get_review_instances(Review.objects.all())
    if request.method == 'GET' and 'name' in request.GET and 'date' in request.GET and 'time' in request.GET:
        name = request.GET['name']
        date = request.GET['date']
        time = request.GET['time']
        reviews = Review.objects.filter(date=date, time=time, reviewer_name=name)
        reviewInstances = get_review_instances(reviews)
        latestReviews = get_review_instances(Review.objects.all())
    for inst in reviewInstances:
        latestReviews = match_instance(inst, latestReviews)
    return render(request, "destination.html", {
        'destinations': reviewInstances,
        'currentUser': request.session.get('currentUser', ''),
        'latest_reviews': latestReviews,
    })


def profile(request):
    common_post_method_handler(request)
    common_get_method_handler(request)
    reviewInstances = []
    if request.method == 'POST' and 'id_input_editprofilephoto' in request.FILES and 'id_input_editbiodata' in request.POST:
        profilePhoto = request.FILES['id_input_editprofilephoto']
        bioData = request.POST['id_input_editbiodata']
        user = User.objects.get(username=request.session.get('currentUser', ''))
        user.profilePhoto = profilePhoto
        user.bioData = bioData
        user.save()
        searchuser = [user]
        reviews = Review.objects.filter(reviewer_name=user.username)
        reviewInstances = get_review_instances(reviews)
    if request.method == 'GET' and request.GET.get('username', '') != '':
        username = request.GET.get('username')
        searchuser = User.objects.filter(username=username)
        reviews = Review.objects.filter(reviewer_name=username)
        reviewInstances = get_review_instances(reviews)
    latest_reviews = get_review_instances(Review.objects.all())
    for inst in reviewInstances:
        latest_reviews = match_instance(inst, latest_reviews)
    return render(request, "profile.html", {
        'currentUser': request.session.get('currentUser', ''),
        'searchUser': searchuser[0],
        'reviewList': reviewInstances,
        'latest_reviews': latest_reviews,
    })
