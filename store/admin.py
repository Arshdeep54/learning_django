from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(models.Customer)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title"]


# admin.site.register(models.Collection)
admin.site.register(models.Address)
