from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Фильтрация опубликованных постов и сортировка"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'

    def get_object(self, queryset=None):
        """Увеличение счетчика просмотров"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj

class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        """Перенаправление на страницу поста после редактирования"""
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
