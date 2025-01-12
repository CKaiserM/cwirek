from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('login/', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('yard_likes/<int:pk>', views.yard_like, name="yard_like"),
    path('yard_dislikes/<int:pk>', views.yard_dislike, name="yard_dislike"),
    path('yard_show/<int:pk>', views.yard_show, name="yard_show"),
    ]
