from django.contrib import admin
from django.urls import path
from . import views
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('yard/', views.YardView.as_view()),
    path('profile_list/', views.ProfileListView.as_view(), name="profile_list"),
    path('profile/<int:pk>', views.ProfileView.as_view(), name="profile"),
    path('profile/<int:pk>/followers', views.FollowView.followers, name="followers"),
    path('profile/<int:pk>/follows', views.FollowView.follows, name="follows"),
    path('login/', views.ProfileView.login_user, name="login"),
    path('logout', views.ProfileView.logout_user, name="logout"),
    path('register/', views.ProfileView.register_user, name="register"),
    path('update_user/', views.ProfileView.update_user, name="update_user"),
    path('yard_likes/<int:pk>', views.YardView.yard_like, name="yard_like"),
    path('yard_dislikes/<int:pk>', views.YardView.yard_dislike, name="yard_dislike"),
    path('yard_show/<int:pk>', views.YardView.yard_show, name="yard_show"),
    path('yard_delete/<int:pk>', views.YardView.yard_delete, name="yard_delete"),
    path('yard_edit/<int:pk>', views.YardView.yard_edit, name="yard_edit"),
    path('yard_search', views.SearchView.yard_search, name="search_yard"),
    path('user_search', views.SearchView.user_search, name="search_user"),
    path('search/', views.SearchView.search, name="search_all"),
    path('follow/<int:pk>', views.FollowView.follow, name="follow"),
    path('unfollow/<int:pk>', views.FollowView.unfollow, name="unfollow"),
    path('yard/<int:pk>/comment', views.PostCommentView.as_view(), name="comment"),
    path('yard/<int:pk>/edit_comment/<int:pc>', views.PostCommentView.comment_edit, name="edit_comment"),
    path('comment_delete/<int:pk>', views.PostCommentView.comment_delete, name="comment_delete"),
    path('comment_like/<int:pk>', views.PostCommentView.comment_like, name="comment_like"),
    path('comment_dislike/<int:pk>', views.PostCommentView.comment_dislike, name="comment_dislike"),
    path('reply_delete/<int:pk>', views.PostReplyView.reply_delete, name="reply_delete"),
    path('reply_like/<int:pk>', views.PostReplyView.reply_like, name="reply_like"),
    path('reply_dislike/<int:pk>', views.PostReplyView.reply_dislike, name="reply_dislike"),
    path('yard/<int:pk>/reply', views.PostReplyView.as_view(), name="reply"),
    path('comment/<int:pk>/edit_reply/<int:pc>', views.PostReplyView.reply_edit, name="edit_reply"),
    path('notifications/', views.notifications, name="notifications"),
]
