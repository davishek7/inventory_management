from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=250,unique=True,null=True,db_index=True)

    def get_absolute_url(self):
        return reverse('inventory:location',args=[self.slug])

    @property
    def total_quantity(self):
        return self.products.all().aggregate(total_qty=Sum('qty')).get('total_qty',0)

    def __str__(self):
        return self.name


class Product(models.Model):
    location = models.ForeignKey(Location,on_delete=models.CASCADE,blank=True,null=True,related_name='products')
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=250,unique=True,null=True,db_index=True)
    qty = models.IntegerField(default = 0)

    def __str__(self):
        return self.name


class Movement(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='movement_products')
    location_from = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='location_from')
    location_to = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='location_to',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    qty = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.location_to:
            return f'{self.qty} {self.product} moved from {self.location_from} to {self.location_to}'
        else:
            return f'{self.qty} {self.product} moved out from {self.location_from}'