from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Panel principal
    # Cambia la línea de 'dashboard/' por esta:
    path('', views.dashboard_vista, name='dashboard'),

    
    # Módulo de Productos
    path('productos/', views.lista_productos_vista, name='productos_list'),
    path('productos/agregar/', views.agregar_producto_vista, name='agregar_producto'),
    
    # Módulos auxiliares
    path('marcas/', views.marcas_list, name='marcas_list'),
    path('categorias/', views.categorias_list, name='categorias_list'),
    
    # NUEVA RUTA DE MOVIMIENTOS
    path('movimientos/', views.movimientos_list, name='movimientos_list'),
]


