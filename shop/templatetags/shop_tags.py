from django import template

from shop.models import Category, Like

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_likes(user):
    likes = Like.objects.filter(user=user)
    products = [like.product for like in likes]
    return products

@register.simple_tag()
def get_likes_count(user):
    likes = Like.objects.filter(user=user)
    products = [like.product for like in likes]
    return len(products)
