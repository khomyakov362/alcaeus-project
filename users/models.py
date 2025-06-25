from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank' : True, 'null' : True}


class UserRoles(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'


class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    description = models.TextField(verbose_name='description', **NULLABLE)

    def __str__(self):
        return str(self.username)
    
    REQUIRED_FIELDS = ['email']


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['id']
