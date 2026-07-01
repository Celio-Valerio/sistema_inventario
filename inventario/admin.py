from django.contrib import admin
from .models import Marca, Categoria, Producto

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'marca', 'categoria', 'precio_venta', 'stock')
    list_filter = ('tipo', 'marca', 'categoria')
    search_fields = ('nombre', 'descripcion')
