from django.shortcuts import get_object_or_404, render
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(pk=self.kwargs['pk'])
        context['title'] = product.title
        products = Product.objects.all()
        data = []
        i = 0
        while i <= 4:
            from random import randint
            random_int = randint(0,len(products)-1)
            product = products[random_int]
            if not product in data:
                data.append(product)
                i = i + 1
        context['products'] = data
        return context


class ProductByCategory(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/category.html"
    paginate_by = 9
    extra_context = {
        "title":"Category"
    }

    def get_queryset(self):
        sort_field = self.request.GET.get("sort")
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        products =  Product.objects.filter(category=category)
        if sort_field:
            products = Product.objects.filter(category=category).order_by(sort_field)
        return products
