from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Admin(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('verifier', 'Verifier'),
        ('communicator', 'Communicator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='verifier')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
        ordering = ['-date_joined']
        db_table = 'admin_users'
        permissions = [
            ("can_view_dashboard", "Can view admin dashboard"),
            ("can_manage_items", "Can manage lost and found items"),
        ]
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username