from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm


# Публичные представления (доступны всем)
class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ContactsView(TemplateView):
    template_name = 'contacts.html'

# Защищенные представления (только для авторизованных)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/auth/login/'  # Редирект для неавторизованных


    def form_valid(self, form):
        """Дополнительная логика перед сохранением"""
        form.instance.created_by = self.request.user  # Привязываем продукт к пользователю
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/auth/login/'


    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


    def dispatch(self, request, *args, **kwargs):
        """Дополнительная проверка прав"""
        obj = self.get_object()
        if obj.created_by != request.user:  # Разрешаем редактирование только автору
            raise PermissionDenied("Вы не можете редактировать этот продукт")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/auth/login/'


    def dispatch(self, request, *args, **kwargs):
        """Дополнительная проверка прав"""
        obj = self.get_object()
        if obj.created_by != request.user:  # Разрешаем удаление только автору
            raise PermissionDenied("Вы не можете удалить этот продукт")
        return super().dispatch(request, *args, **kwargs)

