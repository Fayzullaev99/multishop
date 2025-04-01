from django.contrib import admin
from shop.models import *

admin.site.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id',"title", "image"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(Offer)
admin.site.register(Partner)
class GallerAdmin(admin.TabularInline):
    model = Gallery
    fk_name = 'product'
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [GallerAdmin]
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Like)




















