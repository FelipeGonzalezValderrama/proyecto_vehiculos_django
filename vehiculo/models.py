from django.db import models

class Vehiculo(models.Model):
    MARCA_CHOICES = (
        ('Fiat', 'Fiat'),
        ('Chevrolet', 'Chevrolet'),
        ('Ford', 'Ford'),
        ('Toyota', 'Toyota'),
        ('Mercedes Benz', 'Mercedes Benz'),
        ('BMW', 'BMW'),
        ('MG Motors', 'MG Motors'),
        ('Changan', 'Changan'),
    )

    CATEGORIA_CHOICES = (
        ('Particular', 'Particular'),
        ('Transporte', 'Transporte'),
        ('Carga', 'Carga'),
    )
    
    marca = models.CharField(max_length=20, choices=MARCA_CHOICES, default='Ford')
    modelo = models.CharField(max_length=100)
    serial_carroceria = models.CharField(max_length=50)
    serial_motor = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='Particular')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = (
            ("visualizar_catalogo", "Puede visualizar el catálogo de vehículos"),
        )


    def __str__(self):
        return f"{self.marca} {self.modelo}"
