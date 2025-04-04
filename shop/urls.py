from shop.views import *
from django.urls import path


urlpatterns = [
    path("",Index.as_view(),name="index"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="detail"),
    path("category/<int:pk>/", ProductByCategory.as_view(), name="category"),
    path("likes/", LikeList.as_view(), name="likes"),
    path("likes/<int:pk>/", user_like, name="like"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
]