from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test  # ← ESTA LÍNEA DEBE ESTAR
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from decimal import Decimal
import requests
import json
import uuid
from datetime import datetime, timedelta
from .models import CarritoCompras, CarritoItem, Pedido, DetallePedido, HistorialPrecio, Local, PagoTransbank
import logging

# También agregar la importación de Transbank si la usas
try:
    from transbank.webpay.webpay_plus.transaction import Transaction
    TRANSBANK_AVAILABLE = True
except ImportError:
    TRANSBANK_AVAILABLE = False
    Transaction = None

# Configurar loggers
admin_logger = logging.getLogger('admin_actions')
general_logger = logging.getLogger('catalogo')
# Agregar tarjetaclase PagoTarjeta:
class PagoTarjeta:
    """Modelo temporal para pagos con tarjeta"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def objects(cls):
        return cls
    
    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

# ==================== VISTAS ORIGINALES ====================
def home(request):
    return render(request, "ferreteria/dashboard.html")

def despedirse(request):
    return HttpResponse("<h1> Hasta la vista....baby </h1>")

def ver_inicial(request):
    return render(request,"inicial.html")

def salude(request):
    contexto = {
            'nombre':'Profesor Pino'
        }
    return render(request,"salude.html", contexto)

def ver_clientes(request):
    datos = [
        {'nombre':'Diego Jeldrez', 'correo':'diego@gmail.com'},
        {'nombre':'Cristobal Fuentes', 'correo':'cristobal@gmail.com'},
        {'nombre':'Pablo Figueroa', 'correo':'pablo@gmail.com'},
        {'nombre':'Benjamin Reyes', 'correo':'benjamin@gmail.com'},
        {'nombre':'Alexander Sepulveda', 'correo':'alexander@gmail.com'},
        {'nombre':'Agustin Heinz', 'correo':'agustin@gmail.com'},
        {'nombre':'Mario Garcia', 'correo':'mario@gmail.com'},
    ]
    contexto = {
        'clientes':datos
    }
    return render(request,"ver_clientes.html", contexto)

def obtener_uf_actual():
    url="https://www.mindicador.cl/api/uf/15-05-2025"
    try:
        response = requests.get(url)
        data = response.json()
        uf = data['serie'][0]['valor']
        fecha = data['serie'][0]['fecha']
        return uf, fecha
    except Exception as e:
        return None, str(e)

def leer_uf_actual(request):
    uf, fecha = obtener_uf_actual()
    contexto = {
            'uf':uf,
            'fecha':fecha
        }
    return render(request,"ver_uf.html", contexto)

def obtener_empleados():
    url="http://127.0.0.1:8089/api/empleados"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return None
    
def ver_empleados(request):
    empleados = obtener_empleados()
    contexto = { "datos":empleados}
    return render (request, "ver_empleados.html", contexto)

def obtener_comunas():
    url="http://127.0.0.1:8089/api/comunas"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return None

def ver_comunas(request):
    comunas = obtener_comunas()
    contexto = { "datos":comunas}
    return render (request, "ver_comunas.html", contexto)

def crear_empleado(request):
    if request.method == 'POST':
        comuna_data = {
            "id": request.POST['comuna_id'],
            "nombre": request.POST['comuna_nombre']
        }
        data = {
            "rut": request.POST['rut'],
            "nombre": request.POST['nombre'],
            "telefono": request.POST['telefono'],
            "correo": request.POST['correo'],
            "comuna": comuna_data        }
        requests.post("http://127.0.0.1:8089/api/empleados", json=data)
        return redirect('empleado_exito')
    comunas = requests.get("http://127.0.0.1:8089/api/comunas").json()
    return render(request, 'crear_empleado.html', {"comunas": comunas})

def empleado_exito(request):
    return render(request, 'empleado_exitosos.html')

# ==================== TIENDA FERRETERA - PRODUCTOS ====================
# Funciones para conectar con la API externa en localhost:3309

def obtener_todos_productos():
    """Obtiene todos los productos desde la API externa"""
    url = "http://127.0.0.1:8089/api/productos"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get('productos', [])
        else:
            print(f"API no disponible - Código de estado: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return []

def obtener_producto_por_id(producto_id):
    """Obtiene un producto específico por ID desde la API externa"""
    url = f"http://127.0.0.1:8089/api/productos/{producto_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('producto', data) if isinstance(data, dict) else data
        else:
            print(f"Producto {producto_id} no encontrado en la API")
            return None
    except Exception as e:
        print(f"Error al obtener producto {producto_id}: {e}")
        return None

def crear_producto_api(producto_data):
    """Crea un producto en la API externa"""
    url = "http://127.0.0.1:8089/api/productos"
    try:
        response = requests.post(url, json=producto_data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error al crear producto: {e}")
        return None

def actualizar_producto_api(producto_id, producto_data):
    """Actualiza un producto en la API externa"""
    url = f"http://127.0.0.1:8089/api/productos/{producto_id}"
    try:
        response = requests.put(url, json=producto_data)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error al actualizar producto {producto_id}: {e}")
        return None

def eliminar_producto_api(producto_id):
    """Elimina un producto en la API externa"""
    url = f"http://127.0.0.1:8089/api/productos/{producto_id}"
    try:
        response = requests.delete(url)
        return response.status_code == 200 or response.status_code == 204
    except Exception as e:
        print(f"Error al eliminar producto {producto_id}: {e}")
        return False

def buscar_productos(query):
    """Busca productos por nombre, código o categoría"""
    productos = obtener_todos_productos()
    
    if not query:
        return productos
    
    query = query.lower()
    productos_encontrados = []
    
    for producto in productos:
        if (query in producto['nombre'].lower() or 
            query in producto['codigo'].lower() or 
            query in producto['categoria'].lower() or
            query in producto.get('marca', '').lower()):
            productos_encontrados.append(producto)
    
    return productos_encontrados

# ==================== VISTAS DE PRODUCTOS (Similar a ProductoController.java) ====================

def catalogo_productos(request):
    """Vista principal del catálogo de productos - GET /productos"""
    query = request.GET.get('buscar', '')
    categoria_filtro = request.GET.get('categoria', '')
    
    productos = obtener_todos_productos()
    
    # Filtrar por búsqueda
    if query:
        productos = buscar_productos(query)
    
    # Filtrar por categoría
    if categoria_filtro:
        productos = [p for p in productos if p['categoria'] == categoria_filtro]
    
    # ✅ AGREGAR AQUÍ - Calcular margen para cada producto
    for producto in productos:
        if producto.get('precio_compra') and producto.get('precio_venta'):
            precio_venta = float(producto['precio_venta'])
            precio_compra = float(producto['precio_compra'])
            producto['margen_porcentaje'] = round(((precio_venta - precio_compra) / precio_compra) * 100, 1)
            # ✅ ESTA LÍNEA CALCULA EL VALOR DEL INVENTARIO
            producto['valor_inventario'] = precio_compra * producto.get('stock_actual', 0)
        else:
            producto['margen_porcentaje'] = 0
            producto['valor_inventario'] = 0
    
    # Obtener categorías únicas para el filtro
    todos_productos = obtener_todos_productos()
    categorias = list(set(p['categoria'] for p in todos_productos))
    categorias.sort()
    
    # Paginación
    paginator = Paginator(productos, 8)  # 8 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {
        'productos': page_obj,
        'categorias': categorias,
        'query': query,
        'categoria_filtro': categoria_filtro,
        'total_productos': len(productos)
    }
    
    return render(request, 'ferreteria/catalogo_productos.html', contexto)

def detalle_producto(request, producto_id):
    """Vista detalle de un producto específico - GET /productos/{id}"""
    producto = obtener_producto_por_id(producto_id)
    
    if not producto:
        messages.error(request, 'Producto no encontrado')
        return redirect('catalogo_productos')
    
    # Calcular métricas adicionales con validación de campos
    precio_venta = producto.get('precio_venta', 0)
    precio_compra = producto.get('precio_compra', 0)
    
    if precio_venta and precio_compra and precio_compra > 0:
        margen = round(((precio_venta - precio_compra) / precio_compra) * 100, 2)
        producto['margen_ganancia'] = margen
    else:
        producto['margen_ganancia'] = 0
    
    producto['necesita_restock'] = producto.get('stock_actual', 0) <= producto.get('stock_minimo', 0)
    producto['valor_inventario'] = producto.get('stock_actual', 0) * precio_compra
    
    contexto = {
        'producto': producto
    }
    
    return render(request, 'ferreteria/detalle_producto.html', contexto)

# Agregar decorador y verificación de permisos a todas las funciones de gestión de productos

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def crear_producto(request):
    """Vista para crear un nuevo producto - POST /productos - SOLO ADMINISTRADORES"""
    if request.method == 'POST':
        # Log del intento de creación
        admin_logger.info(f"Admin {request.user.username} intenta crear producto")
        
        # Obtener datos del formulario
        nuevo_producto = {
            'codigo': request.POST.get('codigo'),
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion', ''),
            'categoria': request.POST.get('categoria'),
            'precio_compra': float(request.POST.get('precio_compra', 0)),
            'precio_venta': float(request.POST.get('precio_venta', 0)),
            'stock_actual': int(request.POST.get('stock_actual', 0)),
            'stock_minimo': int(request.POST.get('stock_minimo', 0)),
            'unidad_medida': request.POST.get('unidad_medida', 'unidad'),
            'marca': request.POST.get('marca', ''),
            'proveedor': request.POST.get('proveedor'),
            'estado': request.POST.get('estado', 'activo')
        }
        
        # Validaciones básicas
        if not nuevo_producto['codigo'] or not nuevo_producto['nombre']:
            admin_logger.warning(f"Admin {request.user.username} - Error en validación: campos obligatorios faltantes")
            messages.error(request, 'Código y nombre son obligatorios')
            return render(request, 'ferreteria/crear_producto.html')
        
        # Intentar crear el producto en la API
        resultado = crear_producto_api(nuevo_producto)
        if resultado:
            admin_logger.info(f"Admin {request.user.username} creó producto exitosamente: {nuevo_producto['codigo']} - {nuevo_producto['nombre']}")
            messages.success(request, f'Producto {nuevo_producto["nombre"]} creado exitosamente')
            return redirect('catalogo_productos')
        else:
            admin_logger.error(f"Admin {request.user.username} - Error al crear producto en API: {nuevo_producto['codigo']}")
            messages.error(request, 'Error al crear el producto en la API')
            return render(request, 'ferreteria/crear_producto.html')
    
    # Obtener listas para los selectores
    productos = obtener_todos_productos()
    categorias = list(set(p['categoria'] for p in productos))
    proveedores = list(set(p.get('proveedor', '') for p in productos))
    marcas = list(set(p.get('marca', '') for p in productos))
    
    contexto = {
        'categorias': sorted([c for c in categorias if c]),
        'proveedores': sorted([p for p in proveedores if p]),
        'marcas': sorted([m for m in marcas if m])
    }
    
    return render(request, 'ferreteria/crear_producto.html', contexto)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def editar_producto(request, producto_id):
    """Vista para editar un producto existente con historial de precios"""
    producto = obtener_producto_por_id(producto_id)
    
    if not producto:
        admin_logger.warning(f"Admin {request.user.username} intentó editar producto inexistente: {producto_id}")
        messages.error(request, 'Producto no encontrado')
        return redirect('catalogo_productos')
    
    # Calcular margen si hay precios
    if producto.get('precio_venta') and producto.get('precio_compra'):
        precio_venta = float(producto.get('precio_venta', 0))
        precio_compra = float(producto.get('precio_compra', 0))
        if precio_compra > 0:
            producto['margen_porcentaje'] = round(((precio_venta - precio_compra) / precio_compra) * 100, 2)
        else:
            producto['margen_porcentaje'] = 0
    else:
        producto['margen_porcentaje'] = 0
    
    if request.method == 'POST':
        admin_logger.info(f"Admin {request.user.username} editando producto: {producto_id} - {producto.get('nombre', 'N/A')}")
        
        # Capturar precios anteriores antes de actualizar
        precio_venta_anterior = Decimal(str(producto.get('precio_venta', 0)))
        precio_compra_anterior = Decimal(str(producto.get('precio_compra', 0)))
        precio_venta_nuevo = Decimal(str(request.POST.get('precio_venta', 0)))
        precio_compra_nuevo = Decimal(str(request.POST.get('precio_compra', 0)))
        
        # Obtener datos del formulario
        producto_actualizado = {
            'codigo': request.POST.get('codigo'),
            'nombre': request.POST.get('nombre'),
            'descripcion': request.POST.get('descripcion'),
            'categoria': request.POST.get('categoria'),
            'precio_compra': float(precio_compra_nuevo),
            'precio_venta': float(precio_venta_nuevo),
            'stock_actual': int(request.POST.get('stock_actual', 0)),
            'stock_minimo': int(request.POST.get('stock_minimo', 0)),
            'unidad_medida': request.POST.get('unidad_medida'),
            'marca': request.POST.get('marca'),
            'proveedor': request.POST.get('proveedor'),
            'estado': request.POST.get('estado', 'activo')
        }
        
        # Intentar actualizar en la API
        resultado = actualizar_producto_api(producto_id, producto_actualizado)
        if resultado:
            # Guardar historial de precios si cambió cualquier precio
            if precio_venta_anterior != precio_venta_nuevo or precio_compra_anterior != precio_compra_nuevo:
                HistorialPrecio.objects.create(
                    producto_id=producto_id,
                    producto_codigo=producto.get('codigo', ''),
                    producto_nombre=producto.get('nombre', ''),
                    precio_anterior=precio_venta_anterior,
                    precio_nuevo=precio_venta_nuevo,
                    precio_compra_anterior=precio_compra_anterior,
                    precio_compra_nuevo=precio_compra_nuevo,
                    usuario_modificacion=request.user,
                    razon_cambio=request.POST.get('razon_cambio_precio', 'Actualización de precio')
                )
                admin_logger.info(f"Historial de precio guardado: {producto['nombre']} - Venta: ${precio_venta_anterior} -> ${precio_venta_nuevo}")
            
            admin_logger.info(f"Admin {request.user.username} actualizó producto exitosamente: {producto_id} - {producto_actualizado['nombre']}")
            messages.success(request, f'Producto {producto_actualizado["nombre"]} actualizado exitosamente')
            return redirect('detalle_producto', producto_id=producto_id)
        else:
            admin_logger.error(f"Admin {request.user.username} - Error al actualizar producto: {producto_id}")
            messages.error(request, 'Error al actualizar el producto')
    
    # Obtener historial de precios del producto
    historial_precios = HistorialPrecio.objects.filter(producto_id=producto_id).order_by('-fecha_modificacion')[:10]
    
    # Obtener datos para los selectores
    productos = obtener_todos_productos()
    categorias = list(set(p['categoria'] for p in productos))
    proveedores = list(set(p.get('proveedor', '') for p in productos))
    marcas = list(set(p.get('marca', '') for p in productos))
    
    contexto = {
        'producto': producto,
        'historial_precios': historial_precios,
        'categorias': sorted([c for c in categorias if c]),
        'proveedores': sorted([p for p in proveedores if p]),
        'marcas': sorted([m for m in marcas if m])
    }
    
    return render(request, 'ferreteria/editar_producto.html', contexto)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def eliminar_producto(request, producto_id):
    """Vista para eliminar un producto - DELETE /productos/{id} - SOLO ADMINISTRADORES"""
    if request.method == 'POST':
        producto = obtener_producto_por_id(producto_id)
        
        if producto:
            admin_logger.warning(f"Admin {request.user.username} eliminando producto: {producto_id} - {producto.get('nombre', 'N/A')}")
            
            # Intentar eliminar en la API
            if eliminar_producto_api(producto_id):
                admin_logger.info(f"Admin {request.user.username} eliminó producto exitosamente: {producto_id} - {producto['nombre']}")
                messages.success(request, f'Producto {producto["nombre"]} eliminado exitosamente')
            else:
                admin_logger.error(f"Admin {request.user.username} - Error al eliminar producto: {producto_id}")
                messages.error(request, 'Error al eliminar el producto')
        else:
            admin_logger.warning(f"Admin {request.user.username} intentó eliminar producto inexistente: {producto_id}")
            messages.error(request, 'Producto no encontrado')
    
    return redirect('catalogo_productos')

# También proteger las APIs de creación/edición/eliminación
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def api_crear_producto(request):
    """API endpoint para crear producto - POST /api/productos - SOLO ADMINISTRADORES"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nuevo_producto = {
                'codigo': data.get('codigo'),
                'nombre': data.get('nombre'),
                'descripcion': data.get('descripcion', ''),
                'categoria': data.get('categoria'),
                'precio_compra': float(data.get('precio_compra', 0)),
                'precio_venta': float(data.get('precio_venta', 0)),
                'stock_actual': int(data.get('stock_actual', 0)),
                'stock_minimo': int(data.get('stock_minimo', 0)),
                'unidad_medida': data.get('unidad_medida', 'unidad'),
                'marca': data.get('marca', ''),
                'proveedor': data.get('proveedor'),
                'estado': data.get('estado', 'activo')
            }
            
            # Intentar crear en la API externa
            resultado = crear_producto_api(nuevo_producto)
            if resultado:
                return JsonResponse({'mensaje': 'Producto creado exitosamente', 'producto': resultado}, status=201)
            else:
                return JsonResponse({'error': 'Error al crear producto en la API'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def api_actualizar_producto(request, producto_id):
    """API endpoint para actualizar producto - PUT /api/productos/{id} - SOLO ADMINISTRADORES"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            # Validar que el producto existe
            producto_existente = obtener_producto_por_id(producto_id)
            if not producto_existente:
                return JsonResponse({'error': 'Producto no encontrado'}, status=404)
            
            # Preparar datos actualizados
            producto_actualizado = {
                'codigo': data.get('codigo'),
                'nombre': data.get('nombre'),
                'descripcion': data.get('descripcion', ''),
                'categoria': data.get('categoria'),
                'precio_compra': float(data.get('precio_compra', 0)),
                'precio_venta': float(data.get('precio_venta', 0)),
                'stock_actual': int(data.get('stock_actual', 0)),
                'stock_minimo': int(data.get('stock_minimo', 0)),
                'unidad_medida': data.get('unidad_medida', 'unidad'),
                'marca': data.get('marca', ''),
                'proveedor': data.get('proveedor'),
                'estado': data.get('estado', 'activo')
            }
            
            # Intentar actualizar en la API externa
            resultado = actualizar_producto_api(producto_id, producto_actualizado)
            if resultado:
                return JsonResponse({'mensaje': 'Producto actualizado exitosamente', 'producto': resultado})
            else:
                return JsonResponse({'error': 'Error al actualizar producto en la API'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def api_eliminar_producto(request, producto_id):
    """API endpoint para eliminar producto - DELETE /api/productos/{id} - SOLO ADMINISTRADORES"""
    if request.method == 'DELETE':
        try:
            producto = obtener_producto_por_id(producto_id)
            if not producto:
                return JsonResponse({'error': 'Producto no encontrado'}, status=404)
            
            if eliminar_producto_api(producto_id):
                return JsonResponse({'mensaje': 'Producto eliminado exitosamente'})
            else:
                return JsonResponse({'error': 'Error al eliminar producto'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Agregar import al inicio del archivo si no está
from django.contrib.auth.decorators import user_passes_test

# ==================== API ENDPOINTS (JSON) - Similar a ProductoController ====================

def api_productos_list(request):
    """API endpoint que devuelve todos los productos en formato JSON - GET /api/productos"""
    productos = obtener_todos_productos()
    return JsonResponse({'productos': productos, 'total': len(productos)})

def api_producto_detail(request, producto_id):
    """API endpoint que devuelve un producto específico en JSON - GET /api/productos/{id}"""
    producto = obtener_producto_por_id(producto_id)
    
    if producto:
        return JsonResponse({'producto': producto})
    else:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def api_crear_producto(request):
    """API endpoint para crear producto - POST /api/productos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nuevo_producto = {
                'codigo': data.get('codigo'),
                'nombre': data.get('nombre'),
                'descripcion': data.get('descripcion', ''),
                'categoria': data.get('categoria'),
                'precio_compra': float(data.get('precio_compra', 0)),
                'precio_venta': float(data.get('precio_venta', 0)),
                'stock_actual': int(data.get('stock_actual', 0)),
                'stock_minimo': int(data.get('stock_minimo', 0)),
                'unidad_medida': data.get('unidad_medida', 'unidad'),
                'marca': data.get('marca', ''),
                'proveedor': data.get('proveedor'),
                'estado': data.get('estado', 'activo')
            }
            
            # Intentar crear en la API externa
            resultado = crear_producto_api(nuevo_producto)
            if resultado:
                return JsonResponse({'mensaje': 'Producto creado exitosamente', 'producto': resultado}, status=201)
            else:
                return JsonResponse({'error': 'Error al crear producto en la API'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# ==================== DASHBOARD FERRETERÍA ====================

def dashboard_ferreteria(request):
    """Dashboard principal con estadísticas de la ferretería"""
    productos = obtener_todos_productos()
    
    # Si no hay productos de la API, crear datos de muestra
    if not productos:
        productos = [
            {
                'id': 1,
                'codigo': 'MTL001',
                'nombre': 'Martillo 16oz',
                'categoria': 'Herramientas',
                'precio_compra': 15000,
                'precio_venta': 25000,
                'stock_actual': 25,
                'stock_minimo': 10,
                'estado': 'activo'
            },
            {
                'id': 2,
                'codigo': 'TOR001',
                'nombre': 'Destornillador Phillips',
                'categoria': 'Herramientas',
                'precio_compra': 8000,
                'precio_venta': 12000,
                'stock_actual': 5,
                'stock_minimo': 15,
                'estado': 'activo'
            },
            {
                'id': 3,
                'codigo': 'CLV001',
                'nombre': 'Clavos 2 pulgadas (1kg)',
                'categoria': 'Fijaciones',
                'precio_compra': 3000,
                'precio_venta': 5000,
                'stock_actual': 50,
                'stock_minimo': 20,
                'estado': 'activo'
            },
            {
                'id': 4,
                'codigo': 'PIN001',
                'nombre': 'Pintura Latex Blanca 1L',
                'categoria': 'Pinturas',
                'precio_compra': 8000,
                'precio_venta': 14000,
                'stock_actual': 8,
                'stock_minimo': 12,
                'estado': 'activo'
            },
            {
                'id': 5,
                'codigo': 'TUB001',
                'nombre': 'Tubería PVC 4 pulgadas',
                'categoria': 'Plomería',
                'precio_compra': 12000,
                'precio_venta': 18000,
                'stock_actual': 15,
                'stock_minimo': 10,
                'estado': 'activo'
            },
            {
                'id': 6,
                'codigo': 'CAB001',
                'nombre': 'Cable Eléctrico 12 AWG',
                'categoria': 'Electricidad',
                'precio_compra': 2500,
                'precio_venta': 4000,
                'stock_actual': 3,
                'stock_minimo': 20,
                'estado': 'activo'
            }
        ]
    
    # Estadísticas básicas
    total_productos = len(productos)
    productos_activos = len([p for p in productos if p.get('estado', 'activo') == 'activo'])
    productos_bajo_stock = len([p for p in productos if p.get('stock_actual', 0) <= p.get('stock_minimo', 0)])
    
    # Valor total del inventario
    valor_inventario = sum(p.get('precio_compra', 0) * p.get('stock_actual', 0) for p in productos)
    valor_venta_potencial = sum(p.get('precio_venta', 0) * p.get('stock_actual', 0) for p in productos)
    
    # Productos por categorías
    categorias_stats = {}
    for producto in productos:
        cat = producto.get('categoria', 'Sin Categoría')
        if cat not in categorias_stats:
            categorias_stats[cat] = {'cantidad': 0, 'valor': 0}
        categorias_stats[cat]['cantidad'] += 1
        categorias_stats[cat]['valor'] += producto.get('precio_compra', 0) * producto.get('stock_actual', 0)
    
    # Productos que necesitan restock
    productos_restock = [p for p in productos if p.get('stock_actual', 0) <= p.get('stock_minimo', 0)]
    
    contexto = {
        'total_productos': total_productos,
        'productos_activos': productos_activos,
        'productos_bajo_stock': productos_bajo_stock,
        'valor_inventario': valor_inventario,
        'valor_venta_potencial': valor_venta_potencial,
        'categorias_stats': categorias_stats,
        'productos_restock': productos_restock[:5],  # Solo los primeros 5
        'ganancia_potencial': valor_venta_potencial - valor_inventario
    }
    
    return render(request, 'ferreteria/dashboard.html', contexto)

# ==================== CARRITO DE COMPRAS E-COMMERCE ====================

def obtener_o_crear_carrito(request):
    """Obtiene o crea un carrito para el usuario o sesión"""
    if request.user.is_authenticated:
        carrito, created = CarritoCompras.objects.get_or_create(
            usuario=request.user,
            defaults={}
        )
    else:
        # Para usuarios anónimos, usar la sesión
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        carrito, created = CarritoCompras.objects.get_or_create(
            session_key=session_key,
            usuario=None,
            defaults={'session_key': session_key}
        )
    
    return carrito

def guardar_carrito(request, carrito):
    """El carrito se guarda automáticamente en la base de datos"""
    # Esta función ya no es necesaria pero la mantenemos por compatibilidad
    pass

def agregar_al_carrito(request, producto_id):
    """Agrega un producto al carrito usando modelos de Django"""
    if request.method == 'POST':
        producto = obtener_producto_por_id(producto_id)
        if not producto:
            messages.error(request, 'Producto no encontrado')
            return redirect('catalogo_productos')

        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad <= 0:
            messages.error(request, 'La cantidad debe ser mayor a 0')
            return redirect('detalle_producto', producto_id=producto_id)

        if cantidad > producto.get('stock_actual', 0):
            messages.error(request, f'Solo hay {producto.get("stock_actual", 0)} unidades disponibles')
            return redirect('detalle_producto', producto_id=producto_id)

        carrito = obtener_o_crear_carrito(request)
        
        # Verificar si el producto ya está en el carrito
        item_existente = CarritoItem.objects.filter(carrito=carrito, producto_id=producto_id).first()
        
        if item_existente:
            nueva_cantidad = item_existente.cantidad + cantidad
            if nueva_cantidad > producto.get('stock_actual', 0):
                messages.error(request, f'No hay suficiente stock. Máximo disponible: {producto.get("stock_actual", 0)}')
                return redirect('detalle_producto', producto_id=producto_id)
            item_existente.cantidad = nueva_cantidad
            item_existente.precio_unitario = Decimal(str(producto.get('precio_venta', 0)))
            item_existente.save()
        else:
            # Crear item directamente sin ForeignKey a Producto
            CarritoItem.objects.create(
                carrito=carrito,
                producto_id=producto_id,
                producto_codigo=producto.get('codigo', ''),
                producto_nombre=producto.get('nombre', ''),
                precio_unitario=Decimal(str(producto.get('precio_venta', 0))),
                cantidad=cantidad
            )
        
        messages.success(request, f'{producto.get("nombre")} agregado al carrito')
        return redirect('ver_carrito')
    return redirect('catalogo_productos')


def ver_carrito(request):
    """Muestra el contenido del carrito desde la base de datos"""
    carrito = obtener_o_crear_carrito(request)
    items = []
    total = 0
    cantidad_items = 0
    
    for item in carrito.items.all():
        # Obtener datos actualizados del producto desde la API
        producto_api = obtener_producto_por_id(item.producto_id)
        if producto_api:
            cantidad = min(item.cantidad, producto_api.get('stock_actual', 0))
            precio_actual = Decimal(str(producto_api.get('precio_venta', 0)))
            subtotal = cantidad * precio_actual
            
            items.append({
                'id': item.id,
                'producto': {
                    'id': item.producto_id,
                    'nombre': item.producto_nombre,
                    'codigo': item.producto_codigo,
                    'categoria': producto_api.get('categoria', ''),
                    'precio_venta': precio_actual,
                    'stock_actual': producto_api.get('stock_actual', 0)
                },
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
            cantidad_items += cantidad
    
    iva = total * Decimal('0.19')
    total_con_iva = total + iva
    
    contexto = {
        'items_carrito': items,
        'total': total,
        'iva': iva,
        'total_con_iva': total_con_iva,
        'cantidad_items': cantidad_items,
        'carrito': carrito
    }
    return render(request, 'ferreteria/carrito.html', contexto)


def actualizar_carrito(request, item_id):
    """Actualiza la cantidad de un item en el carrito"""
    if request.method == 'POST':
        try:
            item = CarritoItem.objects.get(id=item_id)
            carrito = obtener_o_crear_carrito(request)
            
            if item.carrito != carrito:
                messages.error(request, 'No tienes permiso para modificar este item')
                return redirect('ver_carrito')
            
            nueva_cantidad = int(request.POST.get('cantidad', 1))
            
            if nueva_cantidad <= 0:
                item.delete()
                # Cambiar esta línea:
                messages.success(request, f'{item.producto_nombre} eliminado del carrito')  # Era: item.producto.nombre
            else:
                # Cambiar esta línea también:
                producto_api = obtener_producto_por_id(item.producto_id)  # Era: item.producto.id
                if producto_api and nueva_cantidad <= producto_api.get('stock_actual', 0):
                    item.cantidad = nueva_cantidad
                    item.precio_unitario = Decimal(str(producto_api.get('precio_venta', 0)))
                    item.save()
                    messages.success(request, 'Cantidad actualizada')
                else:
                    stock_disponible = producto_api.get('stock_actual', 0) if producto_api else 0
                    messages.error(request, f'Stock insuficiente. Disponible: {stock_disponible}')
        
        except CarritoItem.DoesNotExist:
            messages.error(request, 'Item no encontrado')
        except ValueError:
            messages.error(request, 'Cantidad inválida')
    
    return redirect('ver_carrito')

def eliminar_del_carrito(request, item_id):
    """Elimina un item específico del carrito"""
    try:
        item = CarritoItem.objects.get(id=item_id)
        carrito = obtener_o_crear_carrito(request)
        
        if item.carrito == carrito:
            # Cambiar esta línea:
            nombre_producto = item.producto_nombre  # Era: item.producto.nombre
            item.delete()
            messages.success(request, f'{nombre_producto} eliminado del carrito')
        else:
            messages.error(request, 'No tienes permiso para eliminar este item')
    
    except CarritoItem.DoesNotExist:
        messages.error(request, 'Item no encontrado')
    
    return redirect('ver_carrito')

def limpiar_carrito(request):
    """Elimina todos los items del carrito"""
    carrito = obtener_o_crear_carrito(request)
    carrito.items.all().delete()
    messages.success(request, 'Carrito vaciado')
    
    return redirect('ver_carrito')

# ==================== CHECKOUT Y PAGOS ====================

@login_required
def checkout(request):
    """Proceso de checkout - formulario de datos de envío"""
    carrito = obtener_o_crear_carrito(request)
    items = carrito.items.all()
    
    if not items:
        messages.error(request, 'Tu carrito está vacío')
        return redirect('catalogo_productos')
    
    if request.method == 'POST':
        # Procesar datos del formulario
        datos_pedido = {
            'email_cliente': request.POST.get('email_cliente'),
            'nombre_cliente': request.POST.get('nombre_completo'),
            'telefono_cliente': request.POST.get('telefono_cliente', ''),
            'direccion_entrega': request.POST.get('direccion_entrega'),
            'ciudad': request.POST.get('ciudad'),
            'metodo_pago': request.POST.get('metodo_pago'),
            'metodo_entrega': request.POST.get('metodo_entrega', 'domicilio')
        }
        
        # Validaciones básicas
        campos_requeridos = ['email_cliente', 'nombre_cliente', 'metodo_pago', 'metodo_entrega']
        if datos_pedido['metodo_entrega'] == 'domicilio':
            campos_requeridos.extend(['direccion_entrega', 'ciudad'])
        
        if not all(datos_pedido.get(campo) for campo in campos_requeridos):
            messages.error(request, 'Por favor completa todos los campos obligatorios')
            contexto = {
                'carrito': carrito,
                'items_carrito': items,
                'subtotal': carrito.total,
                'iva': carrito.total * Decimal('0.19'),
                'total': carrito.total * Decimal('1.19')
            }
            return render(request, 'ferreteria/checkout.html', contexto)
        
        # Guardar datos en la sesión para el proceso de pago
        request.session['datos_pedido'] = datos_pedido
        
        if datos_pedido['metodo_pago'] in ['tarjeta_credito', 'tarjeta_debito']:
            return redirect('procesar_pago')
        else:
            return redirect('confirmar_pedido')
    
    contexto = {
        'carrito': carrito,
        'items_carrito': items,
        'subtotal': carrito.total,
        'iva': carrito.total * Decimal('0.19'),
        'total': carrito.total * Decimal('1.19'),
        'usuario': request.user
    }
    return render(request, 'ferreteria/checkout.html', contexto)

@login_required
def procesar_pago(request):
    """Procesar pago con Transbank WebPay Plus"""
    carrito = obtener_o_crear_carrito(request)
    datos_pedido = request.session.get('datos_pedido')
    
    if not datos_pedido:
        messages.error(request, 'Datos de pedido no encontrados')
        return redirect('checkout')
    
    if not TRANSBANK_AVAILABLE:
        messages.error(request, 'Sistema de pagos no disponible temporalmente')
        return redirect('checkout')
    
    if request.method == 'POST':
        try:
            # Calcular monto total
            subtotal = carrito.total if hasattr(carrito, 'total') else sum(item.cantidad * item.precio_unitario for item in carrito.items.all())
            iva = subtotal * Decimal('0.19')
            total = subtotal + iva
            
            # Generar orden única
            buy_order = f"FERR-{timezone.now().strftime('%Y%m%d%H%M%S')}-{request.user.id}"
            session_id = request.session.session_key or buy_order
            
            # Configurar Transbank
            from django.conf import settings
            transaction = Transaction()
            
            # Crear transacción con Transbank
            response = transaction.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=int(total),  # Monto en pesos chilenos
                return_url=request.build_absolute_uri('/confirmar-pago-transbank/')
            )
            
            # Crear registro de pago en la base de datos
            pago_pendiente = PagoTransbank.objects.create(
                pedido_id=None,  # Se asignará después de crear el pedido
                buy_order=buy_order,
                session_id=session_id,
                token_ws=response['token'],
                monto=total,
                estado='pendiente',
                ip_cliente=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Guardar datos necesarios en sesión
            request.session['transbank_token'] = response['token']
            request.session['buy_order'] = buy_order
            request.session['pago_id'] = pago_pendiente.id
            
            # Redirigir a Transbank
            return redirect(f"{response['url']}?token_ws={response['token']}")
            
        except Exception as e:
            admin_logger.error(f"Error al procesar pago Transbank: {str(e)}")
            messages.error(request, f'Error al procesar pago: {str(e)}')
            return redirect('checkout')
    
    # Calcular totales para mostrar
    subtotal = carrito.total if hasattr(carrito, 'total') else sum(item.cantidad * item.precio_unitario for item in carrito.items.all())
    iva = subtotal * Decimal('0.19')
    total = subtotal + iva
    
    contexto = {
        'carrito': carrito,
        'items_carrito': carrito.items.all(),
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'datos_pedido': datos_pedido,
        'transbank_disponible': TRANSBANK_AVAILABLE
    }
    
    return render(request, 'ferreteria/pago.html', contexto)

@login_required  
def confirmar_pago_transbank(request):
    """Confirmar pago desde Transbank"""
    token_ws = request.GET.get('token_ws') or request.session.get('transbank_token')
    
    if not token_ws:
        messages.error(request, 'Token de pago no válido')
        return redirect('catalogo_productos')
    
    try:
        # Obtener registro de pago
        pago = PagoTransbank.objects.get(token_ws=token_ws)
        
        if not TRANSBANK_AVAILABLE:
            messages.error(request, 'Sistema de pagos no disponible')
            return redirect('checkout')
        
        # Confirmar transacción con Transbank
        transaction = Transaction()
        response = transaction.commit(token_ws)
        
        # Actualizar registro de pago
        pago.authorization_code = response.get('authorization_code', '')
        pago.response_code = str(response.get('response_code', ''))
        pago.transaction_date = timezone.now()
        pago.accounting_date = response.get('accounting_date', '')
        pago.payment_type_code = response.get('payment_type_code', '')
        pago.card_number = response.get('card_detail', {}).get('card_number', '')[-4:] if response.get('card_detail') else ''
        pago.fecha_procesamiento = timezone.now()
        
        if response.get('status') == 'AUTHORIZED':
            pago.estado = 'autorizado'
            pago.save()
            
            # Pago exitoso, proceder con la confirmación del pedido
            request.session['pago_aprobado'] = True
            request.session['datos_transbank'] = {
                'authorization_code': response.get('authorization_code'),
                'transaction_date': response.get('transaction_date'),
                'card_detail': response.get('card_detail', {}),
                'buy_order': pago.buy_order
            }
            
            messages.success(request, '¡Pago procesado exitosamente!')
            return redirect('confirmar_pedido')
        else:
            pago.estado = 'rechazado'
            pago.save()
            messages.error(request, 'Pago rechazado o cancelado')
            return redirect('checkout')
            
    except PagoTransbank.DoesNotExist:
        messages.error(request, 'Registro de pago no encontrado')
        return redirect('checkout')
    except Exception as e:
        admin_logger.error(f"Error al confirmar pago Transbank: {str(e)}")
        messages.error(request, f'Error al confirmar pago: {str(e)}')
        return redirect('checkout')

# ==================== GESTIÓN DE LOCALES ====================

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_locales(request):
    """Gestión de locales para administradores"""
    locales = Local.objects.all().order_by('nombre')
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        locales = locales.filter(estado=estado_filtro)
    
    ciudad_filtro = request.GET.get('ciudad', '')
    if ciudad_filtro:
        locales = locales.filter(ciudad__icontains=ciudad_filtro)
    
    tipo_filtro = request.GET.get('tipo', '')
    if tipo_filtro:
        locales = locales.filter(tipo=tipo_filtro)
    
    # Paginación
    paginator = Paginator(locales, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas
    stats = {
        'total_locales': Local.objects.count(),
        'locales_activos': Local.objects.filter(estado='activo').count(),
        'locales_mantenimiento': Local.objects.filter(estado='mantenimiento').count(),
        'por_tipo': {}
    }
    
    for tipo, nombre in Local.TIPOS_LOCAL:
        stats['por_tipo'][nombre] = Local.objects.filter(tipo=tipo).count()
    
    contexto = {
        'locales': page_obj,
        'estado_filtro': estado_filtro,
        'ciudad_filtro': ciudad_filtro,
        'tipo_filtro': tipo_filtro,
        'stats': stats,
        'tipos_local': Local.TIPOS_LOCAL,
        'estados_local': Local.ESTADOS_LOCAL
    }
    
    return render(request, 'ferreteria/admin/locales.html', contexto)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def crear_local(request):
    """Crear nuevo local"""
    if request.method == 'POST':
        try:
            local = Local.objects.create(
                nombre=request.POST.get('nombre'),
                codigo=request.POST.get('codigo').upper(),
                tipo=request.POST.get('tipo', 'sucursal'),
                direccion=request.POST.get('direccion'),
                ciudad=request.POST.get('ciudad'),
                region=request.POST.get('region'),
                codigo_postal=request.POST.get('codigo_postal', ''),
                telefono=request.POST.get('telefono', ''),
                email=request.POST.get('email', ''),
                gerente=request.POST.get('gerente', ''),
                horario_atencion=request.POST.get('horario_atencion'),
                permite_retiro=request.POST.get('permite_retiro') == 'on',
                tiene_estacionamiento=request.POST.get('tiene_estacionamiento') == 'on',
                accesible_discapacitados=request.POST.get('accesible_discapacitados') == 'on',
                fecha_apertura=request.POST.get('fecha_apertura'),
                usuario_creacion=request.user,
                latitud=request.POST.get('latitud') or None,
                longitud=request.POST.get('longitud') or None
            )
            
            admin_logger.info(f"Admin {request.user.username} creó local: {local.nombre} ({local.codigo})")
            messages.success(request, f'Local {local.nombre} creado exitosamente')
            return redirect('admin_locales')
            
        except Exception as e:
            admin_logger.error(f"Error al crear local: {str(e)}")
            messages.error(request, f'Error al crear local: {str(e)}')
    
    contexto = {
        'tipos_local': Local.TIPOS_LOCAL,
        'estados_local': Local.ESTADOS_LOCAL
    }
    
    return render(request, 'ferreteria/admin/crear_local.html', contexto)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def editar_local(request, local_id):
    """Editar local existente"""
    local = get_object_or_404(Local, id=local_id)
    
    if request.method == 'POST':
        try:
            local.nombre = request.POST.get('nombre')
            local.codigo = request.POST.get('codigo').upper()
            local.tipo = request.POST.get('tipo')
            local.direccion = request.POST.get('direccion')
            local.ciudad = request.POST.get('ciudad')
            local.region = request.POST.get('region')
            local.codigo_postal = request.POST.get('codigo_postal', '')
            local.telefono = request.POST.get('telefono', '')
            local.email = request.POST.get('email', '')
            local.gerente = request.POST.get('gerente', '')
            local.horario_atencion = request.POST.get('horario_atencion')
            local.permite_retiro = request.POST.get('permite_retiro') == 'on'
            local.tiene_estacionamiento = request.POST.get('tiene_estacionamiento') == 'on'
            local.accesible_discapacitados = request.POST.get('accesible_discapacitados') == 'on'
            local.estado = request.POST.get('estado')
            local.fecha_apertura = request.POST.get('fecha_apertura')
            
            # Coordenadas opcionales
            latitud = request.POST.get('latitud')
            longitud = request.POST.get('longitud')
            local.latitud = Decimal(latitud) if latitud else None
            local.longitud = Decimal(longitud) if longitud else None
            
            local.save()
            
            admin_logger.info(f"Admin {request.user.username} editó local: {local.nombre} ({local.codigo})")
            messages.success(request, f'Local {local.nombre} actualizado exitosamente')
            return redirect('admin_locales')
            
        except Exception as e:
            admin_logger.error(f"Error al editar local: {str(e)}")
            messages.error(request, f'Error al actualizar local: {str(e)}')
    
    contexto = {
        'local': local,
        'tipos_local': Local.TIPOS_LOCAL,
        'estados_local': Local.ESTADOS_LOCAL
    }
    
    return render(request, 'ferreteria/admin/editar_local.html', contexto)

def locales_publicos(request):
    """Vista pública de locales para clientes"""
    locales_activos = Local.objects.filter(estado='activo').order_by('ciudad', 'nombre')
    
    # Agrupar por ciudad
    locales_por_ciudad = {}
    for local in locales_activos:
        if local.ciudad not in locales_por_ciudad:
            locales_por_ciudad[local.ciudad] = []
        locales_por_ciudad[local.ciudad].append(local)
    
    contexto = {
        'locales_por_ciudad': locales_por_ciudad,
        'total_locales': locales_activos.count(),
        'ciudades': sorted(locales_por_ciudad.keys())
    }
    
    return render(request, 'ferreteria/locales.html', contexto)

# ==================== FUNCIONES DE INTEGRACIÓN SPRING BOOT ====================

def sync_productos_springboot(request):
    """Sincroniza productos con el backend de Spring Boot"""
    if request.method == 'POST':
        try:
            productos = obtener_todos_productos()
            return JsonResponse({
                'mensaje': 'Sincronización completada',
                'productos_sincronizados': len(productos),
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def sync_categorias_springboot(request):
    """Sincroniza categorías con el backend de Spring Boot"""
    if request.method == 'POST':
        try:
            productos = obtener_todos_productos()
            categorias = list(set(p.get('categoria', '') for p in productos if p.get('categoria')))
            return JsonResponse({
                'mensaje': 'Categorías sincronizadas',
                'categorias': categorias,
                'total': len(categorias)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def sync_proveedores_springboot(request):
    """Sincroniza proveedores con el backend de Spring Boot"""
    if request.method == 'POST':
        try:
            productos = obtener_todos_productos()
            proveedores = list(set(p.get('proveedor', '') for p in productos if p.get('proveedor')))
            return JsonResponse({
                'mensaje': 'Proveedores sincronizados',
                'proveedores': proveedores,
                'total': len(proveedores)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# ==================== FUNCIONES AUXILIARES Y UTILIDADES ====================

def ajax_comunas_por_region(request, region_id):
    """AJAX para obtener comunas por región"""
    # Implementar según tus datos de comunas
    return JsonResponse({'comunas': []})

def ajax_validar_codigo(request):
    """AJAX para validar código de producto único"""
    codigo = request.GET.get('codigo', '')
    productos = obtener_todos_productos()
    existe = any(p.get('codigo') == codigo for p in productos)
    
    return JsonResponse({'valido': not existe, 'mensaje': 'Código ya existe' if existe else 'Código disponible'})

def ajax_calcular_costo_envio(request):
    """AJAX para calcular costo de envío"""
    # Implementar lógica de cálculo de envío
    return JsonResponse({'costo': 3000})

def webhook_confirmacion_pago(request):
    """Webhook para confirmaciones de pago"""
    if request.method == 'POST':
        # Procesar webhook de pago
        return JsonResponse({'status': 'received'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def sitemap_xml(request):
    """Generar sitemap XML para SEO"""
    from django.http import HttpResponse
    
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{}/</loc>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{}/productos/</loc>
        <priority>0.8</priority>
    </url>
</urlset>'''.format(request.build_absolute_uri('/')[:-1], request.build_absolute_uri('/')[:-1])
    
    return HttpResponse(sitemap_content, content_type='application/xml')

def robots_txt(request):
    """Generar robots.txt para SEO"""
    from django.http import HttpResponse
    
    robots_content = '''User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Sitemap: {}/sitemap.xml'''.format(request.build_absolute_uri('/')[:-1])
    
    return HttpResponse(robots_content, content_type='text/plain')

# ==================== PÁGINAS INFORMATIVAS ====================

def sobre_nosotros(request):
    """Página sobre nosotros"""
    return render(request, 'ferreteria/paginas/sobre_nosotros.html')

def contacto(request):
    """Página de contacto"""
    return render(request, 'ferreteria/paginas/contacto.html')

def politicas_privacidad(request):
    """Página de políticas de privacidad"""
    return render(request, 'ferreteria/paginas/politicas.html')

def terminos_condiciones(request):
    """Página de términos y condiciones"""
    return render(request, 'ferreteria/paginas/terminos.html')

def informacion_envios(request):
    """Página de información de envíos"""
    return render(request, 'ferreteria/paginas/envios.html')

# ==================== HANDLERS DE ERRORES ====================

def error_404(request, exception):
    """Handler personalizado para error 404"""
    return render(request, 'ferreteria/errores/404.html', status=404)

def error_500(request):
    """Handler personalizado para error 500"""
    return render(request, 'ferreteria/errores/500.html', status=500)

def error_403(request, exception):
    """Handler personalizado para error 403"""
    return render(request, 'ferreteria/errores/403.html', status=403)

# ==================== AUTENTICACIÓN DE USUARIOS ====================

def registro_usuario(request):
    """Registro de nuevos usuarios con validaciones completas"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        errores = []

        if not username or len(username) < 3:
            errores.append('El nombre de usuario debe tener al menos 3 caracteres')
        elif User.objects.filter(username=username).exists():
            errores.append('Este nombre de usuario ya está en uso')

        if not email:
            errores.append('El email es obligatorio')
        elif User.objects.filter(email=email).exists():
            errores.append('Este email ya está registrado')

        if not first_name or not last_name:
            errores.append('Nombre y apellido son obligatorios')

        if not password1 or len(password1) < 6:
            errores.append('La contraseña debe tener al menos 6 caracteres')
        elif password1 != password2:
            errores.append('Las contraseñas no coinciden')

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=False,
                    is_superuser=False,
                    is_active=True
                )
                messages.success(request, f'¡Cuenta creada exitosamente para {user.get_full_name()}!')
                from django.contrib.auth import login
                login(request, user)
                transferir_carrito_anonimo(request, user)
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')

    return render(request, 'registration/registro.html')

def transferir_carrito_anonimo(request, user):
    """Transfiere carrito anónimo al usuario registrado"""
    try:
        session_key = request.session.session_key
        if session_key:
            carrito_anonimo = CarritoCompras.objects.filter(
                session_key=session_key,
                usuario=None
            ).first()

            if carrito_anonimo:
                carrito_usuario, created = CarritoCompras.objects.get_or_create(
                    usuario=user,
                    defaults={'activo': True}
                )

                for item in carrito_anonimo.items.all():
                    item_existente = CarritoItem.objects.filter(
                        carrito=carrito_usuario,
                        producto_id=item.producto_id
                    ).first()

                    if item_existente:
                        item_existente.cantidad += item.cantidad
                        item_existente.save()
                    else:
                        item.carrito = carrito_usuario
                        item.save()

                carrito_anonimo.delete()

    except Exception as e:
        print(f"Error transfiriendo carrito: {e}")

@login_required
def perfil_usuario(request):
    """Perfil del usuario logueado con estadísticas"""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # Actualizar datos del perfil
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('perfil_usuario')

    # Obtener estadísticas del usuario
    try:
        pedidos_usuario = Pedido.objects.filter(usuario=request.user)
        total_pedidos = pedidos_usuario.count()
        total_gastado = sum(p.total for p in pedidos_usuario)
        ultimo_pedido = pedidos_usuario.first() if pedidos_usuario.exists() else None
    except:
        total_pedidos = 0
        total_gastado = 0
        ultimo_pedido = None

    contexto = {
        'total_pedidos': total_pedidos,
        'total_gastado': total_gastado,
        'ultimo_pedido': ultimo_pedido
    }

    return render(request, 'registration/perfil.html', contexto)

@login_required
def confirmar_pedido(request):
    """Confirmación final del pedido y creación en la base de datos"""
    carrito = obtener_o_crear_carrito(request)
    datos_pedido = request.session.get('datos_pedido')
    
    if not datos_pedido or not carrito.items.exists():
        messages.error(request, 'No hay datos de pedido o el carrito está vacío')
        return redirect('catalogo_productos')
    
    try:
        # Calcular totales
        subtotal = sum(item.cantidad * item.precio_unitario for item in carrito.items.all())
        iva = subtotal * Decimal('0.19')
        total = subtotal + iva
        
        # Crear pedido
        pedido = Pedido.objects.create(
            usuario=request.user,
            email_cliente=datos_pedido['email_cliente'],
            nombre_cliente=datos_pedido['nombre_cliente'],
            telefono_cliente=datos_pedido.get('telefono_cliente', ''),
            direccion_entrega=datos_pedido.get('direccion_entrega', ''),
            ciudad=datos_pedido.get('ciudad', ''),
            metodo_pago=datos_pedido['metodo_pago'],
            metodo_entrega=datos_pedido['metodo_entrega'],
            subtotal=subtotal,
            iva=iva,
            total=total,
            estado='pendiente'
        )
        
        # Crear detalles del pedido
        for item in carrito.items.all():
            DetallePedido.objects.create(
                pedido=pedido,
                producto_id=item.producto_id,
                producto_codigo=item.producto_codigo,
                producto_nombre=item.producto_nombre,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=item.cantidad * item.precio_unitario
            )
        
        # Limpiar carrito
        carrito.items.all().delete()
        
        # Limpiar sesión
        if 'datos_pedido' in request.session:
            del request.session['datos_pedido']
        
        messages.success(request, f'¡Pedido #{pedido.numero_pedido} creado exitosamente!')
        return redirect('detalle_pedido', pedido_id=pedido.id)
        
    except Exception as e:
        messages.error(request, f'Error al crear el pedido: {str(e)}')
        return redirect('checkout')

@login_required
def detalle_pedido(request, pedido_id):
    """Ver detalle de un pedido específico"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    
    contexto = {
        'pedido': pedido,
        'detalles': detalles
    }
    
    return render(request, 'ferreteria/detalle_pedido.html', contexto)

@login_required
def mis_pedidos(request):
    """Lista de pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    
    # Paginación
    paginator = Paginator(pedidos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {
        'pedidos': page_obj
    }
    
    return render(request, 'ferreteria/mis_pedidos.html', contexto)

# ==================== PANEL DE ADMINISTRACIÓN ====================

@login_required
def admin_dashboard(request):
    """Panel principal de administración"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('home')
    
    # Obtener estadísticas del sistema
    productos = obtener_todos_productos()
    
    # Estadísticas de productos
    stats = {
        'total_productos': len(productos),
        'productos_activos': len([p for p in productos if p.get('estado') == 'activo']),
        'productos_inactivos': len([p for p in productos if p.get('estado') == 'inactivo']),
        'productos_stock_bajo': len([p for p in productos if p.get('stock_actual', 0) <= p.get('stock_minimo', 0)]),
        'valor_inventario': sum(p.get('precio_compra', 0) * p.get('stock_actual', 0) for p in productos),
        'valor_venta_potencial': sum(p.get('precio_venta', 0) * p.get('stock_actual', 0) for p in productos)
    }
    
    # Productos críticos (stock bajo)
    productos_criticos = [p for p in productos if p.get('stock_actual', 0) <= p.get('stock_minimo', 0)][:5]
    
    # Estadísticas de usuarios
    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    staff_usuarios = User.objects.filter(is_staff=True).count()
    
    # Estadísticas de pedidos
    try:
        total_pedidos = Pedido.objects.count()
        pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
        pedidos_recientes = Pedido.objects.order_by('-fecha_pedido')[:5]
    except:
        total_pedidos = 0
        pedidos_pendientes = 0
        pedidos_recientes = []
    
    contexto = {
        'stats': stats,
        'productos_criticos': productos_criticos,
        'ganancia_potencial': stats['valor_venta_potencial'] - stats['valor_inventario'],
        'usuarios_stats': {
            'total': total_usuarios,
            'activos': usuarios_activos,
            'staff': staff_usuarios,
        },
        'pedidos_stats': {
            'total': total_pedidos,
            'pendientes': pedidos_pendientes,
            'recientes': pedidos_recientes
        }
    }
    
    return render(request, 'ferreteria/admin/dashboard.html', contexto)

@login_required
def admin_productos(request):
    """Gestión avanzada de productos para administradores"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('home')
    
    productos = obtener_todos_productos()
    
    # Calcular margen para cada producto
    for producto in productos:
        if producto.get('precio_compra') and producto.get('precio_venta'):
            precio_venta = float(producto['precio_venta'])
            precio_compra = float(producto['precio_compra'])
            producto['margen_porcentaje'] = round(((precio_venta - precio_compra) / precio_compra) * 100, 1)
            producto['valor_inventario'] = precio_compra * producto.get('stock_actual', 0)
        else:
            producto['margen_porcentaje'] = 0
            producto['valor_inventario'] = 0
    
    # Filtros
    categoria_filtro = request.GET.get('categoria', '')
    estado_filtro = request.GET.get('estado', '')
    stock_filtro = request.GET.get('stock', '')
    
    if categoria_filtro:
        productos = [p for p in productos if p.get('categoria') == categoria_filtro]
    
    if estado_filtro:
        productos = [p for p in productos if p.get('estado') == estado_filtro]
    
    if stock_filtro == 'bajo':
        productos = [p for p in productos if p.get('stock_actual', 0) <= p.get('stock_minimo', 0)]
    elif stock_filtro == 'normal':
        productos = [p for p in productos if p.get('stock_actual', 0) > p.get('stock_minimo', 0)]
    elif stock_filtro == 'alto':
        productos = [p for p in productos if p.get('stock_actual', 0) > p.get('stock_minimo', 0) * 2]
    
    # Paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categorías para filtro
    all_productos = obtener_todos_productos()
    categorias = sorted(list(set(p.get('categoria', '') for p in all_productos if p.get('categoria'))))
    
    contexto = {
        'productos': page_obj,
        'categorias': categorias,
        'categoria_filtro': categoria_filtro,
        'estado_filtro': estado_filtro,
        'stock_filtro': stock_filtro
    }
    
    return render(request, 'ferreteria/admin/productos.html', contexto)

@login_required
def admin_pedidos(request):
    """Gestión de pedidos para administradores"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('home')
    
    # Obtener todos los pedidos
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        pedidos = pedidos.filter(estado=estado_filtro)
    
    # Paginación
    paginator = Paginator(pedidos, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {
        'pedidos': page_obj,
        'estado_filtro': estado_filtro
    }
    
    return render(request, 'ferreteria/admin/pedidos.html', contexto)

@login_required
def admin_inventario(request):
    """Gestión de inventario para administradores"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('home')
    
    productos = obtener_todos_productos()
    
    # Análisis de inventario
    productos_con_analisis = []
    for producto in productos:
        precio_compra = producto.get('precio_compra', 0)
        precio_venta = producto.get('precio_venta', 0)
        stock_actual = producto.get('stock_actual', 0)
        stock_minimo = producto.get('stock_minimo', 0)
        
        producto_analizado = producto.copy()
        producto_analizado['valor_inventario'] = precio_compra * stock_actual
        producto_analizado['valor_venta_potencial'] = precio_venta * stock_actual
        producto_analizado['necesita_restock'] = stock_actual <= stock_minimo
        
        productos_con_analisis.append(producto_analizado)
    
    # Estadísticas
    total_valor_inventario = sum(p['valor_inventario'] for p in productos_con_analisis)
    total_valor_venta = sum(p['valor_venta_potencial'] for p in productos_con_analisis)
    productos_criticos = len([p for p in productos_con_analisis if p['necesita_restock']])
    
    contexto = {
        'productos': productos_con_analisis,
        'total_valor_inventario': total_valor_inventario,
        'total_valor_venta': total_valor_venta,
        'ganancia_potencial': total_valor_venta - total_valor_inventario,
        'productos_criticos': productos_criticos
    }
    
    return render(request, 'ferreteria/admin/inventario.html', contexto)

@login_required
def admin_reportes(request):
    """Reportes y estadísticas para administradores"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('home')
    
    productos = obtener_todos_productos()
    
    # Reporte por categorías
    categorias_stats = {}
    for producto in productos:
        categoria = producto.get('categoria', 'Sin Categoría')
        if categoria not in categorias_stats:
            categorias_stats[categoria] = {
                'cantidad': 0, 
                'valor_inventario': 0, 
                'valor_venta': 0,
                'activos': 0
            }
        
        categorias_stats[categoria]['cantidad'] += 1
        categorias_stats[categoria]['valor_inventario'] += producto.get('precio_compra', 0) * producto.get('stock_actual', 0)
        categorias_stats[categoria]['valor_venta'] += producto.get('precio_venta', 0) * producto.get('stock_actual', 0)
        
        if producto.get('estado') == 'activo':
            categorias_stats[categoria]['activos'] += 1

    # Productos más valiosos
    productos_ordenados = sorted(productos, key=lambda x: x.get('precio_venta', 0) * x.get('stock_actual', 0), reverse=True)
    productos_mas_valiosos = productos_ordenados[:10]
    
    # Productos con mayor margen
    productos_con_margen = []
    for producto in productos:
        precio_compra = producto.get('precio_compra', 0)
        precio_venta = producto.get('precio_venta', 0)
        if precio_compra > 0:
            margen = ((precio_venta - precio_compra) / precio_compra) * 100
            producto_copia = producto.copy()
            producto_copia['margen'] = margen
            productos_con_margen.append(producto_copia)
    
    productos_mayor_margen = sorted(productos_con_margen, key=lambda x: x['margen'], reverse=True)[:10]
    
    contexto = {
        'categorias_stats': categorias_stats,
        'productos_mas_valiosos': productos_mas_valiosos,
        'productos_mayor_margen': productos_mayor_margen,
        'total_productos': len(productos),
        'total_categorias': len(categorias_stats)
    }
    
    return render(request, 'ferreteria/admin/reportes.html', contexto)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/')
def admin_cambiar_estado_usuario(request, user_id):
    """Cambiar estado activo/inactivo de un usuario"""
    if request.method == 'POST':
        try:
            usuario = User.objects.get(id=user_id)
            nuevo_estado = not usuario.is_active
            usuario.is_active = nuevo_estado
            usuario.save()
            
            estado_texto = "activado" if nuevo_estado else "desactivado"
            admin_logger.info(f"Admin {request.user.username} {estado_texto} usuario: {usuario.username}")
            messages.success(request, f'Usuario {usuario.username} {estado_texto} exitosamente')
            
        except User.DoesNotExist:
            admin_logger.warning(f"Admin {request.user.username} intentó cambiar estado de usuario inexistente: {user_id}")
            messages.error(request, 'Usuario no encontrado')
        except Exception as e:
            admin_logger.error(f"Error al cambiar estado de usuario: {str(e)}")
            messages.error(request, f'Error al cambiar estado: {str(e)}')
    
    return redirect('admin_usuarios')

@login_required
def admin_usuarios(request):
    """Gestión de usuarios para administradores"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('home')
    
    usuarios = User.objects.all().order_by('-date_joined')
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    if estado_filtro == 'activos':
        usuarios = usuarios.filter(is_active=True)
    elif estado_filtro == 'inactivos':
        usuarios = usuarios.filter(is_active=False)
    elif estado_filtro == 'staff':
        usuarios = usuarios.filter(is_staff=True)
    
    # Paginación
    paginator = Paginator(usuarios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {
        'usuarios': page_obj,
        'estado_filtro': estado_filtro
    }
    
    return render(request, 'ferreteria/admin/usuarios.html', contexto)

# ==================== API ENDPOINTS CARRITO (AJAX) ====================

def api_carrito_resumen(request):
    """API para obtener resumen del carrito - AJAX"""
    try:
        carrito = obtener_o_crear_carrito(request)
        total_items = carrito.items.count()
        total_productos = sum(item.cantidad for item in carrito.items.all())
        
        return JsonResponse({
            'total_items': total_items,
            'total_productos': total_productos,
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)

def api_carrito_items(request):
    """API para obtener items del carrito - AJAX"""
    try:
        carrito = obtener_o_crear_carrito(request)
        items = []
        
        for item in carrito.items.all():
            items.append({
                'id': item.id,
                'producto_id': item.producto_id,
                'producto_nombre': item.producto_nombre,
                'producto_codigo': item.producto_codigo,
                'cantidad': item.cantidad,
                'precio_unitario': float(item.precio_unitario),
                'subtotal': float(item.cantidad * item.precio_unitario)
            })
        
        return JsonResponse({
            'items': items,
            'total_items': len(items),
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)

def api_carrito_total(request):
    """API para obtener total del carrito - AJAX"""
    try:
        carrito = obtener_o_crear_carrito(request)
        subtotal = sum(item.cantidad * item.precio_unitario for item in carrito.items.all())
        iva = subtotal * Decimal('0.19')
        total = subtotal + iva
        
        return JsonResponse({
            'subtotal': float(subtotal),
            'iva': float(iva),
            'total': float(total),
            'cantidad_items': carrito.items.count(),
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)

@csrf_exempt
def api_agregar_carrito(request):
    """API para agregar productos al carrito - AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            cantidad = int(data.get('cantidad', 1))
            
            # Validar producto
            producto = obtener_producto_por_id(producto_id)
            if not producto:
                return JsonResponse({
                    'error': 'Producto no encontrado',
                    'success': False
                }, status=404)
            
            if cantidad > producto.get('stock_actual', 0):
                return JsonResponse({
                    'error': f'Stock insuficiente. Disponible: {producto.get("stock_actual", 0)}',
                    'success': False
                }, status=400)
            
            # Agregar al carrito
            carrito = obtener_o_crear_carrito(request)
            item_existente = CarritoItem.objects.filter(carrito=carrito, producto_id=producto_id).first()
            
            if item_existente:
                nueva_cantidad = item_existente.cantidad + cantidad
                if nueva_cantidad > producto.get('stock_actual', 0):
                    return JsonResponse({
                        'error': f'Stock insuficiente. Máximo disponible: {producto.get("stock_actual", 0)}',
                        'success': False
                    }, status=400)
                item_existente.cantidad = nueva_cantidad
                item_existente.save()
            else:
                CarritoItem.objects.create(
                    carrito=carrito,
                    producto_id=producto_id,
                    producto_codigo=producto.get('codigo', ''),
                    producto_nombre=producto.get('nombre', ''),
                    precio_unitario=Decimal(str(producto.get('precio_venta', 0))),
                    cantidad=cantidad
                )
            
            # Recalcular totales
            total_items = carrito.items.count()
            total_productos = sum(item.cantidad for item in carrito.items.all())
            
            return JsonResponse({
                'mensaje': f'{producto.get("nombre")} agregado al carrito',
                'total_items': total_items,
                'total_productos': total_productos,
                'success': True
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'success': False
            }, status=500)
    
    return JsonResponse({
        'error': 'Método no permitido',
        'success': False
    }, status=405)

def confirmacion_pedido(request, numero_pedido):
    """Vista para mostrar confirmación del pedido"""
    try:
        if request.user.is_authenticated:
            pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido, usuario=request.user)
        else:
            # Para usuarios anónimos, verificar en la sesión
            pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido)
        
        detalles = DetallePedido.objects.filter(pedido=pedido)
        
        contexto = {
            'pedido': pedido,
            'detalles': detalles
        }
        
        return render(request, 'ferreteria/confirmacion_pedido.html', contexto)
        
    except Exception as e:
        messages.error(request, 'Pedido no encontrado')
        return redirect('catalogo_productos')


