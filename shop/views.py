from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from shop.forms import LoginForm, RegisterForm
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
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        products =  Product.objects.filter(category=category)

        sort_field = self.request.GET.get("sort")
        price_field = self.request.GET.getlist("price")
        color_field = self.request.GET.getlist("color")
        size_field = self.request.GET.getlist("size")
        if sort_field:
            products = products.order_by(sort_field)
        if price_field:
            price_fields = {
                '0-100':(0, 100),
                '100-200':(100, 200),
                '200-300':(200, 300),
                '300-400':(300, 400),
                '400-500':(400, 500),
            }
            price_list = [price_fields[pr] for pr in price_field if pr in price_fields ]
            if price_list:
                products = products.filter(
                    price__gte=min(pr[0] for pr in price_list),
                    price__lte=max(pr[1] for pr in price_list)
                    )
        
        if color_field:
            products = products.filter(color__in=color_field)
        
        if size_field:
            products = products.filter(size__in=size_field)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        products =  Product.objects.filter(category=category)
        products_100 = products.filter(price__gte=0,price__lte=100).count()
        products_200 = products.filter(price__gte=100,price__lte=200).count()
        products_300 = products.filter(price__gte=200,price__lte=300).count()
        products_400 = products.filter(price__gte=300,price__lte=400).count()
        products_500 = products.filter(price__gte=400,price__lte=500).count()
        products_black = products.filter(color='black').count()
        products_white = products.filter(color='white').count()
        products_red = products.filter(color='red').count()
        products_green = products.filter(color='green').count()
        products_blue = products.filter(color='blue').count()
        products_xs = products.filter(size='XS').count()
        products_s = products.filter(size='S').count()
        products_m = products.filter(size='M').count()
        products_l = products.filter(size='L').count()
        products_xl = products.filter(size='XL').count()
        data = {
            "products_100":products_100,
            "products_200":products_200,
            "products_300":products_300,
            "products_400":products_400,
            "products_500":products_500,
            "products_black":products_black,
            "products_white":products_white,
            "products_red":products_red,
            "products_green":products_green,
            "products_blue":products_blue,
            "products_xs":products_xs,
            "products_s":products_s,
            "products_m":products_m,
            "products_l":products_l,
            "products_xl":products_xl,
        }
        context.update(data)
        return context

def user_login(request):
    form = LoginForm()
    context = {
        "title":"Sign In",
        "form":form
    }
    return render(request, "shop/login.html", context)

def user_register(request):
    form = RegisterForm()
    context = {
        "title":"Sign Up",
        "form":form
    }
    return render(request, "shop/register.html", context)

def signup(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        return redirect("login")
    else:
        return redirect("register")

def signin(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request,user)
        return redirect("index")
    else:
        return redirect("login")

def signout(request):
    logout(request)
    return redirect("login")
