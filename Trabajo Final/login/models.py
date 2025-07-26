from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserProfile(models.Model):
    """
    Perfil de usuario para almacenar información específica de roles para facilitar las consultas
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_director = models.BooleanField(_('is director'), default=False)
    is_secretary = models.BooleanField(_('is secretary'), default=False)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"