from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)

        # Отправляем приветственное письмо
        send_mail(
            subject='Добро пожаловать в наш магазин!',
            message='Спасибо за регистрацию.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[form.cleaned_data['email']],
            fail_silently=False,
        )
        return response
