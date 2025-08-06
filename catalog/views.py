from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm
from django.views.decorators.cache import cache_page
from .services import get_products_by_category
from .services import get_all_products

class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'products'


    def get_queryset(self):
        return get_all_products()


    def get_queryset(self):
        """Только опубликованные продукты"""
        return Product.objects.filter(publish_status='published')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    @method_decorator(cache_page(60 * 15))  # Кеш на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ContactsView(TemplateView):
    template_name = 'contacts.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/auth/login/'


    def form_valid(self, form):
        """Автоматическое назначение владельца"""
        form.instance.owner = self.request.user
        form.instance.publish_status = 'moderation'
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/auth/login/'


    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


    def dispatch(self, request, *args, **kwargs):
        """Проверка прав: владелец или модератор"""
        product = self.get_object()
        if not (request.user == product.owner or
                request.user.has_perm('catalog.can_change_publish_status')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/auth/login/'


    def dispatch(self, request, *args, **kwargs):
        """Проверка прав: владелец или модератор"""
        product = self.get_object()
        if not (request.user == product.owner or
                request.user.has_perm('catalog.delete_product')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'


    def get_queryset(self):
        return get_products_by_category(self.kwargs['category_id'])