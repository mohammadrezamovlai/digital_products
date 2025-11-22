from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import AppUser
from utlis.validators import validate_sku








class Package(models.Model):
    title = models.CharField(_('package'),max_length=50)
    sku = models.CharField(_('suck keeping unit'),max_length=20,validators=[validate_sku],db_index=True)
    description = models.TextField(_('description'),blank=True)
    avatar = models.ImageField(_('avatar'),blank=True,upload_to='packages/')
    is_enable = models.BooleanField(_('is_enable'),default=True)
    price = models.PositiveIntegerField(_('price'))
    duration = models.DurationField(_('duration'),blank=True,null=True)
    created_time = models.DateTimeField(_('created_time'),auto_now_add=True)
    update_time = models.DateTimeField(_('update_time'),auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = _('Package')
        verbose_name_plural = _('packages')

class Subscription(models.Model):
    user = models.ForeignKey('users.Appuser',related_name='%(class)s',on_delete=models.CASCADE)
    package = models.ForeignKey(Package,related_name='%(class)s',on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created_time'),auto_now_add=True)
    expire_time = models.DateTimeField(_('expire_time'),auto_now=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('Subscripion')
        verbose_name_plural = _('subscriptions')