from django.contrib import admin
from .models import Product,Location,Movement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','location','qty']
    prepopulated_fields={'slug':('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display=['name','total_quantity']
    prepopulated_fields={'slug':('name',)}

    def total_quantity(self,obj):
        if obj.total_quantity:
            return obj.total_quantity
        else:
            return 0


admin.site.register(Movement)
