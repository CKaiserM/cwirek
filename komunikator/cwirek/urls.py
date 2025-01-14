from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('profile/<int:pk>/followers', views.followers, name="followers"),
    path('profile/<int:pk>/follows', views.follows, name="follows"),
    path('login/', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('yard_likes/<int:pk>', views.yard_like, name="yard_like"),
    path('yard_dislikes/<int:pk>', views.yard_dislike, name="yard_dislike"),
    path('yard_show/<int:pk>', views.yard_show, name="yard_show"),
    path('yard_delete/<int:pk>', views.yard_delete, name="yard_delete"),
    path('yard_edit/<int:pk>', views.yard_edit, name="yard_edit"),
    path('yard_search', views.yard_search, name="search_yard"),
    path('user_search', views.user_search, name="search_user"),
    path('search/', views.search, name="search"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    ]
