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
        # Captura los datos digitados en tu formulario
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        marca_id = request.POST.get('marca')
        categoria_id = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')

        # 1. Crea y guarda el producto de forma directa en Postgres
        nuevo_producto = Producto.objects.create(
            nombre=nombre,
            tipo=tipo,
            marca_id=marca_id,
            categoria_id=categoria_id,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock
        )

        # 2. AUTOMATIZACIÓN: Crea automáticamente el registro de entrada en el Kardex
        HistorialStock.objects.create(
            producto=nuevo_producto,
            tipo='ENTRADA',
            cantidad=int(stock),
            motivo="Inventario Inicial (Registro de nuevo producto)"
        )

        return redirect('inventario:productos_list')

    # Si es una consulta normal, carga las listas desplegables
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
