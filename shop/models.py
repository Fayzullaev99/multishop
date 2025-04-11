from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email must be fill")
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs) 
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be True is_staff")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be True is_superuser")
        
        return self.create_user(email=email,password=password, **kwargs)

class CustomUser(AbstractUser):
    COUNTRY_CHOICES = [
        ("UZB","UZBEKISTAN"),
        ("KAZ","KAZAKHSTAN"),
        ("KYR","KYRGYZSTAN"),
    ]
    username = None
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default="UZB")
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def get_photo(self):
        try:
            return self.image.url
        except:
            return "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg"

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="subcategory")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"

class Offer(models.Model):
    title = models.CharField(max_length=100)
    percent = models.IntegerField(default=10)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

class Product(models.Model):
    SIZE_CHOICES = [
        ("XS","EXTRA SMALL"),
        ("S","SMALL"),
        ("M","MEDIUM"),
        ("L","LARGE"),
        ("XL","EXTRA LARGE"),
    ]
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sale = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField(default="The description is not available")
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default="M")
    color = models.CharField(max_length=30, blank=True, null=True)
    info = models.TextField(default="The information is not available")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=10)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_first_photo(self):
        if self.photos:
            try:
                return self.photos.first().image.url
            except:
                return "https://thumbs.dreamstime.com/b/no-image-available-icon-sign-isolated-white-background-simple-vector-logo-no-image-available-icon-sign-isolated-white-271600539.jpg"
        else:
            return "https://thumbs.dreamstime.com/b/no-image-available-icon-sign-isolated-white-background-simple-vector-logo-no-image-available-icon-sign-isolated-white-271600539.jpg"

    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

class Partner(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.full_name

class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="baskets")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="basket_items")

    class Meta:
        unique_together = ("user","product")

    def __str__(self):
        return self.user.email
        
    def get_total_quantity(self):
        basket_products = self.basketproduct_set.all()
        total_quantity = sum([product.quantity for product in basket_products])
        return total_quantity
    
    def get_total_price(self):
        basket_products = self.basketproduct_set.all()
        total_price = sum([product.get_total_price for product in basket_products])
        return total_price
    
class BasketProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    
    def get_total_price(self):
        if self.product.sale:
            return self.quantity * self.product.sale
        return self.quantity * self.product.price
    