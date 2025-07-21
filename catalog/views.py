from django.views.generic import ListView, DetailView, TemplateView
from catalog.models import Product

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ContactsView(TemplateView):
    template_name = 'contacts.html'
