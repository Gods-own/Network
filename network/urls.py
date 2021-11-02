
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addpost", views.add_post, name="addPost"),
    path("person/<int:user_id>", views.person, name="person"),
    path("followingspost", views.followings_posts, name="followingsPost"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("editpost/<int:post_id>", views.edit_post, name="editPost"),
    path("settings", views.editProfile, name="settings"),
    path("update", views.update_profile, name="update"),
    path("comments/<int:post_id>", views.comment, name="comments"),

            #    API ROUTES
    path("like/<int:post_id>", views.like_post, name="like"),
    path("isliked/<int:post_id>", views.isliked, name="isliked"),
]
