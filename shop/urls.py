from shop.views import *
from django.urls import path


urlpatterns = [
    path("",Index.as_view(),name="index"),
    path("products/<int:pk>/", ProductDetail.as_view(),name="detail")
]