from django.db import models
from django.core.exceptions import ValidationError

class statusClient(models.TextChoices):
    prospecto = 'Prospecto'
    cliente = 'Cliente'
    inactivo = 'Inactivo'


def validarTelefono(telefono):
    if not telefono.isdigit():
        raise ValidationError('El número de telefono solo puede contener números')

## validar numero telefonico 

class Cliente(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    company = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=10, blank=True, validators=[validarTelefono])
    status = models.CharField(
        max_length=20,
        choices=statusClient.choices,
        default=statusClient.prospecto,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, null= False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)


    def __str__(self):
        return self.name
