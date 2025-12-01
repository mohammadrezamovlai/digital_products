from django.db import models
from django.utils.translation import gettext_lazy as _
from subscriptions.models import Package
from utlis.validators import validate_phone_number


class Gateway(models.Model):
    title = models.CharField(_('title'),max_length=50)
    description = models.TextField(_('description'),blank=True)
    avatar = models.ImageField(_('avatar'),blank=True,upload_to='gateway/')
    is_enable = models.BooleanField(_('is_enable'),default=True)
    credentials = models.TextField(_('credentials'),blank=True)
    created_time = models.DateTimeField(_('created_time'),auto_now_add=True)
    update_time = models.DateTimeField(_('update_time'),auto_now=True)

    class Meta:
        db_table = 'gateway'
        verbose_name = _('Gateway')
        verbose_name_plural =_('Gateways')
    


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = (
        (STATUS_VOID,_('Void')),
        (STATUS_PAID,_('Paid')),
        (STATUS_ERROR,_('Error')),
        (STATUS_CANCELED,_('Canceled')),
        (STATUS_REFUNDED,_('Refunded')),
    )
    STATUS_TRANSLATIONS = {
        STATUS_VOID:_('payment could not proccesed'),
        STATUS_PAID:_('payment succesful'),
        STATUS_ERROR:_('paymnet error'),
        STATUS_CANCELED:_('payment canceled by user'),
        STATUS_REFUNDED:_('this payment has bin refunded'),
    }
    user = models.ForeignKey('users.User',verbose_name=_('user'),related_name='%(class)s',on_delete=models.CASCADE)
    package = models.ForeignKey('subscriptions.Package',verbose_name=_('package'),related_name='%(class)s',on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway,verbose_name=_('gateway'),related_name='%(class)s',on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(_('price'),default=0)
    status = models.PositiveSmallIntegerField(_('status'),choices=STATUS_CHOICES,default=STATUS_VOID,db_index=True)
    device_uuid = models.CharField(_('device_uuid'),max_length=40,blank=True)
    token = models.CharField(max_length=255)
    phone_number = models.BigIntegerField(_('phone_number'),validators=[validate_phone_number],db_index=True)
    consumed_code = models.PositiveIntegerField(_('consumed refrence code '),null=True,db_index=True)
    created_time = models.DateTimeField(_('created_time'),auto_now_add=True,db_index=True)
    update_time = models.DateTimeField(_('update_time'),auto_now=True)


    class Meta:
        db_table = 'payment'
        verbose_name = _('Payment')
        verbose_name_plural =_('Payments')


