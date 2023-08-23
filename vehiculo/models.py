from django.db import models


class Vehiculo(models.Model):
    MARCA_CHOICES = (
        ("Alfa Romeo", "Alfa Romeo"),
        ("Audi", "Audi"),
        ("BMW", "BMW"),
        ("Changan", "Changan"),
        ("Chevrolet", "Chevrolet"),
        ("Fiat", "Fiat"),
        ("Ford", "Ford"),
        ("Hyundai", "Hyundai"),
        ("Kia", "Kia"),
        ("Mazda", "Mazda"),
        ("Mercedes Benz", "Mercedes Benz"),
        ("MG Motors", "MG Motors"),
        ("Mitsubishi", "Mitsubishi"),
        ("Nissan", "Nissan"),
        ("Peugeot", "Peugeot"),
        ("Suzuki", "Suzuki"),
        ("Toyota", "Toyota"),
        ("Volkswagen", "Volkswagen"),
    )

    CATEGORIA_CHOICES = (
        ("Particular", "Particular"),
        ("Transporte", "Transporte"),
        ("Carga", "Carga"),
    )

    ANNIO_CHOICES = (
        ("2000", "2000"),
        ("2001", "2001"),
        ("2002", "2002"),
        ("2003", "2003"),
        ("2004", "2004"),
        ("2005", "2005"),
        ("2006", "2006"),
        ("2007", "2007"),
        ("2008", "2008"),
        ("2009", "2009"),
        ("2010", "2010"),
        ("2011", "2011"),
        ("2012", "2012"),
        ("2013", "2013"),
        ("2014", "2014"),
        ("2015", "2015"),
        ("2016", "2016"),
        ("2017", "2017"),
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
    )

    marca = models.CharField(max_length=20, choices=MARCA_CHOICES, default="Ford")
    modelo = models.CharField(max_length=100)
    serial_carroceria = models.CharField(max_length=50)
    serial_motor = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default="Particular" )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    año = models.CharField(max_length=4, choices=ANNIO_CHOICES, default="2000")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("visualizar_catalogo", "Puede visualizar el catálogo de vehículos"),
        )

    def __str__(self):
        return f"{self.marca} {self.modelo}"
