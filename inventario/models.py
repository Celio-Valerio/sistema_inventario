from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Marca")

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_PRODUCTO_CHOICES = [
        ('ROPA', 'Ropa Deportiva / Casual'),
        ('CALZADO', 'Calzado (Tenis, Tacos, Burros)'),
        ('ACCESORIO', 'Accesorios (Lociones, Fajas, Otros)'),
    ]

    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES, verbose_name="Tipo de Producto")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name="Marca")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoría")
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Compra")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock = models.IntegerField(default=0, verbose_name="Cantidad en Inventario")
    talla = models.CharField(max_length=20, blank=True, null=True, verbose_name="Talla / Tamaño (Opcional)")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.marca.nombre})"
