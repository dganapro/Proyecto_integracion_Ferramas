from django.urls import path
from . import views

urlpatterns = [
    # ==================== PÁGINA PRINCIPAL ====================
    path('', views.dashboard_ferreteria, name='home'),
    path('dashboard/', views.dashboard_ferreteria, name='dashboard'),
    
    # ==================== PRODUCTOS ====================
    path('productos/', views.catalogo_productos, name='catalogo_productos'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    
    # ==================== CARRITO ====================
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.limpiar_carrito, name='vaciar_carrito'),
    
    # ==================== CHECKOUT ====================
    path('checkout/', views.checkout, name='checkout'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('confirmar-pago-transbank/', views.confirmar_pago_transbank, name='confirmar_pago_transbank'),
    
    # ==================== AUTENTICACIÓN ====================
    path('registro/', views.registro_usuario, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # ==================== API AJAX CARRITO (para solucionar 404) ====================
    path('api/carrito/resumen/', views.api_carrito_resumen, name='api_carrito_resumen'),
    path('api/carrito/items/', views.api_carrito_items, name='api_carrito_items'),
    path('api/carrito/total/', views.api_carrito_total, name='api_carrito_total'),
    path('api/carrito/agregar/', views.api_agregar_carrito, name='api_agregar_carrito'),
    
    
    # ==================== PANEL ADMIN ====================
    path('admin-ferreteria/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-ferreteria/productos/', views.admin_productos, name='admin_productos'),
    path('admin-ferreteria/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin-ferreteria/inventario/', views.admin_inventario, name='admin_inventario'),
    path('admin-ferreteria/reportes/', views.admin_reportes, name='admin_reportes'),
    path('admin-ferreteria/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin-ferreteria/usuarios/cambiar-estado/<int:user_id>/', views.admin_cambiar_estado_usuario, name='admin_cambiar_estado_usuario'),
    
    # ==================== LOCALES ====================
    path('locales/', views.locales_publicos, name='locales_publicos'),
    path('admin-ferreteria/locales/', views.admin_locales, name='admin_locales'),
    path('admin-ferreteria/locales/crear/', views.crear_local, name='crear_local'),
    path('admin-ferreteria/locales/editar/<int:local_id>/', views.editar_local, name='editar_local'),
    
    # ==================== VISTAS ORIGINALES ====================
    path('chao/', views.despedirse),
    path('saludar/', views.salude),
    path('clientes/', views.ver_clientes),
    path('uf/', views.leer_uf_actual),
    path('empleados/', views.ver_empleados),
    path('comunas/', views.ver_comunas),
    path('empleados/crear/', views.crear_empleado),
    path('empleados/exito/', views.empleado_exito, name="empleado_exito"),

    
]