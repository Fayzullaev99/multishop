from django.shortcuts import render
from django.views.generic import ListView, DetailView

from shop.models import *

class Index(ListView):
    model = SubCategory
    context_object_name = "subcategories"
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        offers = Offer.objects.all()
        products = Product.objects.all()
        partners = Partner.objects.all()
        data = {
            "categories":categories,
            "subcategories":subcategories,
            "offers":offers,
            "featured_products":products[8:],
            "recent_products":products[:8],
            "partners":partners,
        }
        context["data"] = data
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "shop/detail.html"

