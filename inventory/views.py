from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.contrib import messages
from django.db.models import Sum
from .models import Product, Location, Movement
from .forms import ProductForm, LocationForm, MovementForm


class ProductListView(ListView):
    model = Product
    template_name='all_products.html'
    context_object_name='products'

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_qty"] = self.get_queryset().aggregate(total_qty=Sum('qty')).get('total_qty',0)
        return context
    
    
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_product.html'
    fields = ('qty',)
    success_url = reverse_lazy('inventory:products')


class LocationListView(ListView):
    model = Location
    template_name = 'index.html'
    context_object_name = 'locations'
    success_url = reverse_lazy('inventory:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LocationForm()
        return context


class LocationCreateView(FormView):
    model = Location
    template_name = 'index.html'
    form_class = LocationForm
    success_url = reverse_lazy('inventory:index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.slug = slugify(form.instance.name)
            if Location.objects.filter(slug=form.instance.slug).exists():
                messages.warning(self.request,f'{form.instance.name} already exist!')
            else:
                form.save()
                messages.success(self.request,f'{form.instance.name} added successfully!')
                return redirect('/')
            return self.form_valid(form)
        else:
            messages.warning(self.request,'Something went wrong!')
            return redirect('/')
            return self.form_invalid(form)

    def form_valid(self,form):
        return super().form_valid(form)


class LocationDetailView(FormMixin,DetailView):
    model = Location
    context_object_name = 'location'
    form_class = ProductForm
    template_name = 'location.html'

    def get_success_url(self):
        return reverse('inventory:location', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context['location'].products.filter(qty__gt=0)
        context['total_quantity'] = context['location'].total_quantity
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.location = self.object
            form.instance.slug = slugify(form.instance.name)
            if Product.objects.filter(slug=form.instance.slug).exists():
                messages.warning(self.request,f'{form.instance.name} already exist!')
            else:
                form.save()
                messages.success(self.request,f'{form.instance.name} added successfully!')
            return self.form_valid(form)
        else:
            messages.warning(self.request,'Something went wrong!')
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


def add_movement(request,slug,location_slug):
    product = get_object_or_404(Product,slug=slug)
    location = get_object_or_404(Location,slug=location_slug)
    form = MovementForm()
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.product = product
            movement.location_from = location
            location_to = form.cleaned_data.get('location_to')
            quantity = product.qty
            if location_to != location:
                product.location = location_to
                movement.qty = quantity
                product.save()
                movement.save()
                messages.success(request,'Product moved successfully!')
                return redirect(location)
            else:
                messages.warning(request,'Can not move to the same location!')
                return HttpResponseRedirect(f'/move/{product.slug}/{location.slug}/')
        else:
            messages.warning(request,'Something went wrong!')
            return redirect(location)
    context = {'product':product,'location':location,'form':form}
    return render(request,'add_movement.html',context)


def move_out(request,slug,location_slug):
    product = get_object_or_404(Product,slug=slug)
    location = get_object_or_404(Location,slug=location_slug)

    if product.qty < 1:
        return redirect(location)
    else:
        if request.method == 'POST':
            movement = Movement.objects.create(product = product,location_from=location,qty=product.qty)
            movement.save()
            product.qty -= product.qty
            product.save()
            messages.success(request,f'{product.name} successfully moved out!')
            return redirect(location)
    context = {'location':location,'product':product}
    return render(request,'moveout.html',context)





    
