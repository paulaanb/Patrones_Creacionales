from tabnanny import verbose
from django.db import models

from django.contrib.auth import get_user_model #devuelve el usuario activo actual
from django.db.models import F,Sum, FloatField  # para calcular el total de una orden de pedido
from menu.models import Combo

User=get_user_model()

# Create your models here.

class Peticion(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) # Cuando se elimine un usuario sus pedidos se eliminirán en cascada
    created_at=models.DateTimeField(auto_now_add=True)   #Para le fecha de pedido automática

    @property
    def total(self):
        return self.lineapeticion_set.aggregate(

            total=Sum(F("precio")*F("cantidad"), output_field=FloatField())

        )["total"] or FloatField(0)

    def __str__(self):
        return self.id


    class Meta:
        db_table='peticion'
        verbose_name='peticion'
        verbose_name_plural='peticiones'
        ordering=['id']


class LineaPeticion(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    combo=models.ForeignKey(Combo, on_delete=models.CASCADE)
    peticion=models.ForeignKey(Peticion, on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} de {self.combo.nombre}'

    class Meta:
        db_table='lineapeticiones'
        verbose_name='Línea Peticion'
        verbose_name_plural='Líneas Peticiones'
        ordering=['id']

