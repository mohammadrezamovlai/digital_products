import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class AppUser(models.Model):

    ROLE_CHOICES = [
        ('customer', 'مشتری'),
        ('seller', 'فروشنده'),
        ('trainer', 'مربی'),
        ('admin', 'مدیر داخلی سیستم'),
    ]

    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
        ('other', 'سایر'),
    ]
    username = models.CharField(max_length=150,unique=True, verbose_name="نام کاربری")
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, unique=True, verbose_name="شماره موبایل")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="ایمیل")
    password = models.CharField(max_length=255, verbose_name="رمز عبور هش‌شده")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تولد")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="عکس پروفایل")
    bio = models.TextField(blank=True, null=True, verbose_name="بیوگرافی کوتاه")
    about = models.TextField(blank=True, null=True, verbose_name="درباره کاربر")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True, verbose_name="فعال است؟")
    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده؟")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت‌نام")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییرات")
    last_seen = models.DateTimeField(blank=True, null=True, verbose_name="آخرین فعالیت")
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="آخرین آی‌پی ورود")
    last_device = models.CharField(max_length=120, blank=True, null=True, verbose_name="آخرین دستگاه ورود")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def update_last_seen(self, ip=None, device=None):
        self.last_seen = timezone.now()
        if ip:
            self.last_login_ip = ip
        if device:
            self.last_device = device
        self.save(update_fields=['last_seen', 'last_login_ip', 'last_device'])

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ['-created_at']
