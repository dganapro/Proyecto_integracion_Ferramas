import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

# Configurar logger para acciones administrativas
admin_logger = logging.getLogger('admin_actions')

class AdminActionLoggingMiddleware(MiddlewareMixin):
    """Middleware para registrar acciones administrativas"""
    
    def process_request(self, request):
        # URLs que requieren logging
        admin_urls = [
            'crear_producto', 'editar_producto', 'eliminar_producto',
            'api_crear_producto', 'api_actualizar_producto', 'api_eliminar_producto',
            'admin_dashboard', 'admin_productos', 'admin_usuarios', 'admin_inventario',
            'admin_pedidos', 'admin_reportes', 'admin_desactivar_usuario'
        ]
        
        if request.user.is_authenticated and request.user.is_staff:
            if any(url in request.path for url in admin_urls):
                admin_logger.info(
                    f"Admin {request.user.username} accedió a {request.path} "
                    f"desde IP {request.META.get('REMOTE_ADDR', 'unknown')} "
                    f"- Método: {request.method} - Timestamp: {timezone.now()}"
                )
        
        return None
    
    def process_response(self, request, response):
        """Log de respuestas para acciones críticas"""
        admin_urls = [
            'crear_producto', 'editar_producto', 'eliminar_producto',
            'api_crear_producto', 'api_actualizar_producto', 'api_eliminar_producto'
        ]
        
        if (request.user.is_authenticated and request.user.is_staff and 
            any(url in request.path for url in admin_urls) and 
            request.method in ['POST', 'PUT', 'DELETE']):
            
            status_msg = "ÉXITO" if 200 <= response.status_code < 300 else "ERROR"
            admin_logger.info(
                f"Admin {request.user.username} - {status_msg} - "
                f"Status: {response.status_code} - Path: {request.path}"
            )
        
        return response

class RoleMiddleware:
    """Middleware para agregar información de roles al request"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Agregar información de rol al usuario si está autenticado
        if request.user.is_authenticated:
            request.user.es_admin = request.user.is_staff
            request.user.es_superadmin = request.user.is_superuser
            request.user.es_cliente = not request.user.is_staff
            
            # Agregar permisos específicos
            request.user.puede_editar_productos = request.user.is_staff
            request.user.puede_ver_reportes = request.user.is_staff
            request.user.puede_gestionar_usuarios = request.user.is_superuser
            request.user.puede_ver_logs = request.user.is_staff
        
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Log de acceso a vistas sensibles para administradores
        if request.user.is_authenticated and request.user.is_staff:
            admin_views = [
                'admin_dashboard', 'admin_productos', 'admin_usuarios', 
                'admin_inventario', 'admin_reportes', 'admin_logs',
                'crear_producto', 'editar_producto', 'admin_locales'
            ]
            
            if view_func.__name__ in admin_views:
                import logging
                admin_logger = logging.getLogger('admin_actions')
                admin_logger.info(f"Admin {request.user.username} accedió a vista: {view_func.__name__}")
        
        return None
