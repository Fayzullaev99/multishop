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


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

class Partner(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)