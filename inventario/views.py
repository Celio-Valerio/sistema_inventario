from django.shortcuts import render
from .models import Producto
from django.db.models import Sum, F

def dashboard_vista(request):
    # Consultas directas a PostgreSQL mediante el ORM de Django
    total_productos = Producto.objects.count()
    stock_total = Producto.objects.aggregate(total=Sum('stock'))['total'] or 0
    
    # Calcula la inversión multiplicando el precio de compra por la cantidad en stock de cada producto
    inversion_total = Producto.objects.all().aggregate(
        total=Sum(F('precio_compra') * F('stock'))
    )['total'] or 0

    # Obtiene los últimos 5 artículos registrados
    productos_recientes = Producto.objects.order_by('-fecha_ingreso')[:5]

    contexto = {
        'total_productos': total_productos,
        'stock_total': stock_total,
        'inversion_total': inversion_total,
        'productos_recientes': productos_recientes,
    }
    return render(request, 'inventario/dashboard.html', contexto)
from django.shortcuts import redirect
from .models import Marca, Categoria

def lista_productos_vista(request):
    productos = Producto.objects.all().order_by('-fecha_ingreso')
    return render(request, 'inventario/productos.html', {'productos': productos})


from .models import Producto, Marca, Categoria, HistorialStock
from django.shortcuts import render, redirect

def agregar_producto_vista(request):
    if request.method == 'POST':
        # Captura segura de los datos desde las etiquetas name de la plantilla HTML
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        marca_id = request.POST.get('marca')
        categoria_id = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')

        # 1. Inserción directa vinculando las llaves foráneas a las marcas/categorías de Postgres
        nuevo_producto = Producto.objects.create(
            nombre=nombre,
            tipo=tipo,
            marca_id=marca_id,
            categoria_id=categoria_id,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock
        )

        # 2. Automatización del Kardex: Genera la Entrada de Inventario Inicial asociada
        HistorialStock.objects.create(
            producto=nuevo_producto,
            tipo='ENTRADA',
            cantidad=int(stock),
            motivo="Inventario Inicial (Registro de nuevo producto)"
        )

        return redirect('inventario:productos_list')

    # Al cargar la pantalla limpia, enviamos los catálogos para llenar las opciones select
    contexto = {
        'marcas': Marca.objects.all(),
        'categorias': Categoria.objects.all()
    }
    return render(request, 'inventario/agregar_producto.html', contexto)


    # Si es una consulta normal, carga las listas desplegables
    contexto = {
        'marcas': Marca.objects.all(),
        'categorias': Categoria.objects.all()
    }
    return render(request, 'inventario/agregar_producto.html', contexto)
def marcas_list(request):
    marcas = Marca.objects.all()
    return render(request, 'inventario/marcas.html', {'marcas': marcas})

def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'inventario/categorias.html', {'categorias': categorias})

def movimientos_list(request):
    movimientos = HistorialStock.objects.all().order_by('-fecha')
    return render(request, 'inventario/movimientos.html', {'movimientos': movimientos})

from django.shortcuts import render, redirect, get_object_or_404

# VISTA PARA EDITAR UN PRODUCTO EXISTENTE
def editar_producto_vista(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.tipo = request.POST.get('tipo')
        producto.marca_id = request.POST.get('marca')
        producto.categoria_id = request.POST.get('categoria')
        producto.precio_compra = request.POST.get('precio_compra')
        producto.precio_venta = request.POST.get('precio_venta')
        
        # Guardamos el stock viejo para comparar si hubo cambios manuales
        stock_nuevo = int(request.POST.get('stock'))
        diferencia = stock_nuevo - producto.stock
        
        if diferencia != 0:
            tipo_mov = 'ENTRADA' if diferencia > 0 else 'SALIDA'
            HistorialStock.objects.create(
                producto=producto,
                tipo=tipo_mov,
                cantidad=abs(diferencia),
                motivo="Ajuste manual al editar especificaciones del producto"
            )
        
        producto.stock = stock_nuevo
        producto.save()
        return redirect('inventario:productos_list')

    contexto = {
        'producto': producto,
        'marcas': Marca.objects.all(),
        'categorias': Categoria.objects.all()
    }
    # Usará el mismo formulario de agregar, adaptado para edición
    return render(request, 'inventario/agregar_producto.html', contexto)


# VISTA PARA ELIMINAR UN PRODUCTO DEFINITIVAMENTE
def eliminar_producto_vista(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('inventario:productos_list')
