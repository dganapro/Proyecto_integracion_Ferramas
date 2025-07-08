from django.urls import path
from . import views

urlpatterns = [
    # ==================== PÁGINAS PRINCIPALES ====================
    path('', views.dashboard_ferreteria, name='home'),
    
    # ==================== PÁGINAS INFORMATIVAS (FALTANTES) ====================
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('politicas-privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    path('informacion-envios/', views.informacion_envios, name='informacion_envios'),
    
    # ==================== PRODUCTOS ====================
    path('productos/', views.catalogo_productos, name='catalogo_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    
    # ==================== CARRITO ====================
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    
    # ==================== CHECKOUT Y PEDIDOS ====================
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('confirmacion/<str:numero_pedido>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    # ==================== AUTENTICACIÓN ====================
    path('registro/', views.registro_usuario, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # ==================== ADMINISTRACIÓN ====================
    path('admin-ferreteria/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-ferreteria/productos/', views.admin_productos, name='admin_productos'),
    path('admin-ferreteria/inventario/', views.admin_inventario, name='admin_inventario'),
    path('admin-ferreteria/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin-ferreteria/reportes/', views.admin_reportes, name='admin_reportes'),
    path('admin-ferreteria/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin-ferreteria/usuarios/cambiar-estado/<int:user_id>/', views.admin_cambiar_estado_usuario, name='admin_cambiar_estado_usuario'),
    
    # ==================== LOCALES ====================
    path('locales/', views.locales_publicos, name='locales_publicos'),
    path('admin-ferreteria/locales/', views.admin_locales, name='admin_locales'),
    path('admin-ferreteria/locales/crear/', views.crear_local, name='crear_local'),
    path('admin-ferreteria/locales/editar/<int:local_id>/', views.editar_local, name='editar_local'),
    
    # ==================== API ENDPOINTS ====================
    path('api/productos/', views.api_productos_list, name='api_productos_list'),
    path('api/productos/<int:producto_id>/', views.api_producto_detail, name='api_producto_detail'),
    path('api/carrito/resumen/', views.api_carrito_resumen, name='api_carrito_resumen'),
    path('api/carrito/items/', views.api_carrito_items, name='api_carrito_items'),
    path('api/carrito/total/', views.api_carrito_total, name='api_carrito_total'),
    path('api/carrito/agregar/', views.api_agregar_carrito, name='api_agregar_carrito'),
    
    # ==================== BÚSQUEDA ====================
    path('busqueda-avanzada/', views.busqueda_avanzada, name='busqueda_avanzada'),
    
    # ==================== VISTAS ORIGINALES ====================
    path('chao/', views.despedirse),
    path('saludar/', views.salude),
    path('clientes/', views.ver_clientes),
    path('uf/', views.leer_uf_actual),
    path('empleados/', views.ver_empleados),
    path('empleados/crear/', views.crear_empleado),
    path('empleados/exito/', views.empleado_exito, name='empleado_exito'),
    path('comunas/', views.ver_comunas),
    
    # ==================== UTILIDADES ====================
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
]

# URLs para manejo de errores (se configuran en settings.py)
handler404 = 'catalogo.views.error_404_view'
handler500 = 'catalogo.views.error_500_view'
handler403 = 'catalogo.views.error_403_view'