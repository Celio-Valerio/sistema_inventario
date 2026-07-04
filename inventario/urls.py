from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Panel principal
    path('', views.dashboard_vista, name='dashboard'),
    
    # Módulo de Productos
    path('productos/', views.lista_productos_vista, name='productos_list'),
    path('productos/agregar/', views.agregar_producto_vista, name='agregar_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto_vista, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto_vista, name='eliminar_producto'),
    
    # Módulos auxiliares
    path('marcas/', views.marcas_list, name='marcas_list'),
    path('categorias/', views.categorias_list, name='categorias_list'),
    
    # Ruta de Movimientos
    path('movimientos/', views.movimientos_list, name='movimientos_list'),
]


