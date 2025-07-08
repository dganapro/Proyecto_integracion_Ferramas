from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# ==================== MODELOS PARA E-COMMERCE FERRETERÍA ====================

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    marca = models.CharField(max_length=100, blank=True, null=True)
    codigo_producto = models.CharField(max_length=50, unique=True, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    @property
    def esta_disponible(self):
        return self.activo and self.stock > 0

class CarritoCompras(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Carrito de Compras"
        verbose_name_plural = "Carritos de Compras"
        db_table = 'catalogo_carrito'
    
    def __str__(self):
        if self.usuario:
            return f"Carrito de {self.usuario.username}"
        return f"Carrito anónimo {self.session_key}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def cantidad_items(self):
        """Número total de items en el carrito"""
        return self.items.count()
    
    @property
    def total_productos(self):
        """Cantidad total de productos (sumando cantidades)"""
        return sum(item.cantidad for item in self.items.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(CarritoCompras, on_delete=models.CASCADE, related_name='items')
    # No usar ForeignKey a Producto, solo campos individuales
    producto_id = models.IntegerField()
    producto_codigo = models.CharField(max_length=50)
    producto_nombre = models.CharField(max_length=200)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        db_table = 'catalogo_carrito_item'
        unique_together = ['carrito', 'producto_id']
    
    def __str__(self):
        return f"{self.producto_nombre} x {self.cantidad}"  # Cambiar self.producto.nombre por self.producto_nombre
    
    @property
    def subtotal(self):
        """Subtotal del item (precio * cantidad)"""
        return self.precio_unitario * self.cantidad
    
    def save(self, *args, **kwargs):
        """Override save para validaciones"""
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        super().save(*args, **kwargs)

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
    ]
    
    METODOS_ENTREGA = [
        ('retiro', 'Retiro en Tienda'),
        ('despacho', 'Despacho a Domicilio'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    numero_pedido = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    
    # Información del cliente
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20, blank=True)
    
    # Información de entrega - AGREGAR DEFAULT AQUÍ
    metodo_entrega = models.CharField(
        max_length=20, 
        choices=METODOS_ENTREGA,
        default='despacho'  # ← AGREGAR ESTE DEFAULT
    )
    direccion_entrega = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    
    # Información de pago - AGREGAR DEFAULT AQUÍ TAMBIÉN
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODOS_PAGO,
        default='efectivo'  # ← AGREGAR ESTE DEFAULT
    )
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Fechas
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateTimeField(blank=True, null=True)
    fecha_entrega_real = models.DateTimeField(blank=True, null=True)
    
    # Notas
    notas_cliente = models.TextField(blank=True, null=True)
    notas_internas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']
        db_table = 'catalogo_pedido'
    
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.nombre_cliente}"
    
    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            import uuid
            self.numero_pedido = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    # Cambiar de ForeignKey a IntegerField para consistencia con CarritoItem
    # producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    producto_id = models.IntegerField()
    producto_codigo = models.CharField(max_length=50)
    producto_nombre = models.CharField(max_length=200)
    producto_categoria = models.CharField(max_length=100, blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles del Pedido"
        db_table = 'catalogo_detalle_pedido'
    
    def __str__(self):
        return f"{self.producto_nombre} x {self.cantidad}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

class PagoTarjeta(models.Model):
    """Modelo para pagos con tarjeta de crédito/débito"""
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    numero_tarjeta_enmascarado = models.CharField(max_length=19, default='**** **** **** 0000')  # ✅ AGREGAR DEFAULT
    tipo_tarjeta = models.CharField(max_length=20, default='visa')  # ✅ AGREGAR DEFAULT
    banco_emisor = models.CharField(max_length=100, blank=True, null=True)
    codigo_autorizacion = models.CharField(max_length=10, default='000000')  # ✅ AGREGAR DEFAULT
    numero_transaccion = models.CharField(max_length=20, unique=True, default='TXN000000')  # ✅ AGREGAR DEFAULT
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ✅ AGREGAR DEFAULT
    estado = models.CharField(max_length=20, default='pendiente')
    
    # Metadatos (ya tienen default)
    ip_cliente = models.GenericIPAddressField(default='127.0.0.1')
    user_agent = models.TextField(default='Unknown')
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'catalogo_pagotarjeta'
        verbose_name = 'Pago Tarjeta'
        verbose_name_plural = 'Pagos Tarjeta'
        ordering = ['-fecha_transaccion']
    
    def __str__(self):
        return f"Pago {self.numero_transaccion} - {self.estado}"

class HistorialPrecio(models.Model):
    """Modelo para trackear cambios de precios en productos"""
    producto_id = models.IntegerField(help_text="ID del producto en la API externa")
    producto_codigo = models.CharField(max_length=50)
    producto_nombre = models.CharField(max_length=200)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra_anterior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_compra_nuevo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    razon_cambio = models.TextField(blank=True, null=True, help_text="Motivo del cambio de precio")
    
    class Meta:
        verbose_name = "Historial de Precio"
        verbose_name_plural = "Historial de Precios"
        ordering = ['-fecha_modificacion']
        indexes = [
            models.Index(fields=['producto_id', '-fecha_modificacion']),
            models.Index(fields=['usuario_modificacion', '-fecha_modificacion']),
        ]
    
    def __str__(self):
        return f"{self.producto_nombre} - {self.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def diferencia_precio(self):
        """Calcula la diferencia de precio"""
        return self.precio_nuevo - self.precio_anterior
    
    @property
    def porcentaje_cambio(self):
        """Calcula el porcentaje de cambio"""
        if self.precio_anterior > 0:
            return ((self.precio_nuevo - self.precio_anterior) / self.precio_anterior) * 100
        return 0

class Local(models.Model):
    """Modelo para gestionar locales/sucursales de la ferretería"""
    TIPOS_LOCAL = [
        ('sucursal', 'Sucursal'),
        ('bodega', 'Bodega'),
        ('showroom', 'Showroom'),
        ('centro_distribucion', 'Centro de Distribución'),
    ]
    
    ESTADOS_LOCAL = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('cerrado_temporal', 'Cerrado Temporalmente'),
        ('inactivo', 'Inactivo'),
    ]
    
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10, unique=True, help_text="Código único del local")
    tipo = models.CharField(max_length=25, choices=TIPOS_LOCAL, default='sucursal')
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    gerente = models.CharField(max_length=200, blank=True)
    horario_atencion = models.TextField(help_text="Ej: Lunes a Viernes 9:00-18:00, Sábados 9:00-14:00")
    permite_retiro = models.BooleanField(default=True, help_text="¿Permite retiro de productos?")
    tiene_estacionamiento = models.BooleanField(default=False)
    accesible_discapacitados = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS_LOCAL, default='activo')
    fecha_apertura = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locales_creados')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locales"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['estado', 'ciudad']),
            models.Index(fields=['tipo', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.ciudad}"
    
    @property
    def direccion_completa(self):
        """Devuelve la dirección completa formateada"""
        return f"{self.direccion}, {self.ciudad}, {self.region}"
    
    def es_activo(self):
        """Verifica si el local está activo"""
        return self.estado == 'activo'

class PagoTransbank(models.Model):
    """Modelo para registrar pagos con Transbank WebPay Plus"""
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, null=True, blank=True)
    buy_order = models.CharField(max_length=26, unique=True)
    session_id = models.CharField(max_length=61)
    token_ws = models.CharField(max_length=64)
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    
    # Estados: pendiente, autorizado, rechazado, anulado
    estado = models.CharField(max_length=20, default='pendiente')
    
    # Datos de respuesta de Transbank
    authorization_code = models.CharField(max_length=6, blank=True, null=True)
    response_code = models.CharField(max_length=2, blank=True, null=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    accounting_date = models.CharField(max_length=4, blank=True, null=True)
    payment_type_code = models.CharField(max_length=2, blank=True, null=True)
    card_number = models.CharField(max_length=4, blank=True, null=True)  # Solo últimos 4 dígitos
    
    # Metadatos
    ip_cliente = models.GenericIPAddressField(default='127.0.0.1')  # ✅ AGREGAR DEFAULT
    user_agent = models.TextField(default='Unknown')  # ✅ AGREGAR DEFAULT
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'catalogo_pagotransbank'
        verbose_name = 'Pago Transbank'
        verbose_name_plural = 'Pagos Transbank'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Pago {self.buy_order} - {self.estado}"

# Modelo para almacenar imágenes de productos subidas por los usuarios
class ProductoImagen(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True)
    imagen = models.ImageField(upload_to='productos/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

