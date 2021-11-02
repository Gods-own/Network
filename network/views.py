from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts, Liked, Comments, Following, NoFollows

from .forms import CreatePosts, PostImage

# function to view all posts
def index(request):
    posts = Posts.objects.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        profile = User.objects.get(username=request.user)
        context = {
        'page_obj' : page_obj,
        'profile': profile,
        'active': 'active'
         }
    else:
        context = {
        'page_obj' : page_obj,
        'active': 'active'
         }
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if not email:
            return render(request, "network/register.html", {
                "message": "Please input your email."
            })
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })  
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        nofollow = NoFollows.objects.create(fuser=user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# function to create a post
@login_required
def add_post(request):
    # This query is for the profile navigation link to take the user to their profile it is in all
    # view functions which is used in the navigation
    profile = User.objects.get(username=request.user)

    if request.method == "POST":
        postform = CreatePosts(request.POST)
        imageform = PostImage(request.POST)
        if postform.is_valid() and imageform.is_valid():
            thepost = postform.cleaned_data["thepost"]
            thepic = imageform.cleaned_data["thepic"]
        if thepic:
            p = Posts.objects.create(poster=request.user, post=thepost, picture=thepic)
        else:
            p = Posts.objects.create(poster=request.user, post=thepost)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/newPost.html", {
            "form1": CreatePosts(),
            "form2": PostImage(),
            "profile": profile,
            'active2': 'active'
        })


# function to edit a post
@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        post = Posts.objects.get(poster=request.user, pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.post = data["post"]
        if data.get("picture") is not None:
            post.picture = data["picture"]
        post.save()
        return JsonResponse({"message": "Done."}, status=200)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)        

# function to view a user's profile
def person(request, user_id):
    if request.user.is_authenticated:
        profile = User.objects.get(username=request.user)
        user = User.objects.get(pk=user_id)
        posts = Posts.objects.order_by("-timestamp").filter(poster=user)
        number_follows = NoFollows.objects.get(fuser=user)
        result = Following.objects.filter(followee=user, curuser=request.user).exists()
        is_following = False
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        if result == True:
            following = Following.objects.get(followee=user, curuser=request.user)
            is_following = following.follo
            return render(request, "network/profile.html", {
            "posts": posts,
            "numbers": number_follows,
            "user": user, 
            "is_following": is_following,
            "page_obj" : page_obj,
            "profile": profile,
            'active3': 'active'
        })
        return render(request, "network/profile.html", {
            "posts": posts,
            "numbers": number_follows,
            "user": user, 
            "is_following": is_following,
            "page_obj" : page_obj,
            "profile": profile,
            'active3': 'active'
        })
    else:
        return HttpResponseRedirect(reverse("login"))

# Function to render the settings page
def editProfile(request):
    profile = User.objects.get(username=request.user)
    return render(request, "network/settings.html", {
        "profile": profile,
        'active4': 'active'
    })

# function to update changes made on profile from settings page
def update_profile(request):
    user = User.objects.get(username=request.user)
    username = request.POST.get('username', None)
    imageurl = request.POST.get('imageurl', None)
    checkusername = User.objects.filter(username=username).exists()
    if checkusername == True:
        message = "Username already exists.Choose another one!"    
        return render(request, "network/settings.html", {
        "profile": user,
        'active4': 'active',
        'message' : message
    })
    if username != None:
        user.username = username
        user.save()
    if imageurl != None:
        user.userImage = imageurl
        user.save()
    return HttpResponseRedirect(reverse("person", kwargs={'user_id': user.id }))        

# function to view posts of users that a user follows
@login_required
def followings_posts(request):
    profile = User.objects.get(username=request.user)
    followings = Following.objects.filter(curuser=request.user)
    theids = []
    for following in followings:
        theid = following.followee
        theids.append(theid)
    posts = Posts.objects.order_by("-timestamp").filter(poster__in=theids)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj' : page_obj, 'profile': profile, 'active1': 'active'}
    return render(request, "network/followPost.html", context)

# function to follow a user
@login_required
def follow(request, user_id):
    user = User.objects.get(pk=user_id)
    results = Following.objects.filter(followee=user, curuser=request.user).exists()
    nofollows = NoFollows.objects.get(fuser=user)
    currentuser = NoFollows.objects.get(fuser=request.user)
    nofollows.nofollowers = nofollows.nofollowers + 1
    currentuser.nofollowing = currentuser.nofollowing + 1
    nofollows.save()
    currentuser.save()
    if results == True:
        updatefollowing = Following.objects.get(followee=user, curuser=request.user)
        updatefollowing.follo = True
        updatefollowing.save()
    else:
        Following.objects.create(followee=user, curuser=request.user, follo=True)
    return HttpResponseRedirect(reverse("person", kwargs={'user_id': user_id }))

# function to unfollow a user
@login_required
def unfollow(request, user_id):
    user = User.objects.get(pk=user_id)
    Following.objects.get(followee=user, curuser=request.user).delete()
    nofollows = NoFollows.objects.get(fuser=user)
    currentuser = NoFollows.objects.get(fuser=request.user)
    nofollows.nofollowers = nofollows.nofollowers - 1
    currentuser.nofollowing = currentuser.nofollowing - 1
    nofollows.save()
    currentuser.save()
    return HttpResponseRedirect(reverse("person", kwargs={'user_id': user_id }))

# function to comment on a post
def comment(request, post_id):
    if request.user.is_authenticated:
        post = Posts.objects.get(pk=post_id)
        profile = User.objects.get(username=request.user)
        if request.method == 'POST':
            thecomment = request.POST['text']
            add_comment = Comments.objects.create(posting=post, person=request.user, comment=thecomment)
            comments = Comments.objects.filter(posting=post)
            post.nocomments = post.nocomments + 1
            post.save()
            return render(request, "network/comments.html", {
            "comments": comments,
            "post": post,
            "profile": profile,
            })
        else:
            comments = Comments.objects.filter(posting=post)
            return render(request, "network/comments.html", {
            "comments": comments,
            "post": post,
            "profile": profile,
            })
    else:
        return HttpResponseRedirect(reverse("login"))

# function to like and unlike a post
@csrf_exempt
@login_required
def like_post(request, post_id):

    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        liked = Liked.objects.filter(liker=request.user, pose=post).exists()
        if liked == False:
            Liked.objects.create(liker=request.user, pose=post, liked=True)
            post.like = post.like + 1
            post.save()
            return JsonResponse({"message": "done."}, status=200)
        else:
            # check if a post is liked or unliked by a particular user inorder to know
            # whether to increment or decrement the number of likes
            checklike = Liked.objects.get(liker=request.user, pose=post)
            if checklike.liked == False:
                checklike.liked = True
                checklike.save()
                post.like = post.like + 1
                post.save()
                return JsonResponse({"message": "done."}, status=200)
            
            else:
                checklike.liked = False
                checklike.save()
                post.like = post.like - 1
                post.save()
                return JsonResponse({"message": "done."}, status=200)

# function to check if a post is liked by a particular user
@csrf_exempt
@login_required
def isliked(request, post_id):
    post = Posts.objects.get(pk=post_id)
    try:
        liked = Liked.objects.get(liker=request.user, pose=post)
    except Liked.DoesNotExist:
        return JsonResponse({"liked": False}, status=200)
    
    return JsonResponse({"liked": liked.liked}, status=200)

