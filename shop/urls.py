from shop.views import *
from django.urls import path


urlpatterns = [
    path("",Index.as_view(),name="index"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="detail"),
    path("category/<int:pk>/", ProductByCategory.as_view(), name="category"),
    path("login/", user_login, name="login"),
    path("register", user_register, name="register"),
    path("signin/", signin, name="signin"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
]