from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        ADMIN = 'admin', 'Administrador'

    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.CLIENTE,
    )

    def es_admin(self):
        return self.rol == self.Rol.ADMIN

    def __str__(self):
        return self.username