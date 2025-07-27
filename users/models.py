from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # Убираем username, используем email для входа
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Дополнительные поля
    avatar = models.ImageField(
        _('avatar'),
        upload_to='users/avatars/',
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        null=True
    )
    country = models.CharField(
        _('country'),
        max_length=100,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'  # Авторизация по email
    REQUIRED_FIELDS = []      # Убираем обязательный username

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

