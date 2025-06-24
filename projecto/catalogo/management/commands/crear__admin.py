from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Crea usuarios administradores y de ejemplo para la ferretería'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Nombre de usuario del admin')
        parser.add_argument('--email', type=str, help='Email del admin')
        parser.add_argument('--password', type=str, help='Contraseña del admin')

    def handle(self, *args, **options):
        self.stdout.write('🔧 Creando sistema de usuarios para Ferretería El Martillo...')
        
        # Datos por defecto para el administrador principal
        username = options.get('username') or 'admin_ferreteria'
        email = options.get('email') or 'admin@ferreteriamartillo.com'
        password = options.get('password') or 'FerramAS2024!'
        
        # Crear superusuario principal
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'⚠️  El usuario {username} ya existe')
            admin_user = User.objects.get(username=username)
        else:
            admin_user = User.objects.create(
                username=username,
                email=email,
                first_name='Administrador',
                last_name='Principal',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                password=make_password(password)
            )
            self.stdout.write(f'✅ Superusuario creado: {username}')
        
        # Crear usuarios adicionales del sistema
        usuarios_sistema = [
            {
                'username': 'vendedor_ferreteria',
                'email': 'vendedor@ferreteriamartillo.com',
                'first_name': 'Juan Carlos',
                'last_name': 'Vendedor',
                'password': 'vendedor123',
                'is_staff': True,
                'is_superuser': False,
                'tipo': 'Staff'
            },
            {
                'username': 'supervisor_tienda',
                'email': 'supervisor@ferreteriamartillo.com',
                'first_name': 'María Elena',
                'last_name': 'Supervisor',
                'password': 'supervisor123',
                'is_staff': True,
                'is_superuser': False,
                'tipo': 'Staff'
            },
            {
                'username': 'cliente_empresa',
                'email': 'empresa@construcciones.cl',
                'first_name': 'Construcciones',
                'last_name': 'Los Andes',
                'password': 'empresa123',
                'is_staff': False,
                'is_superuser': False,
                'tipo': 'Cliente Empresa'
            },
            {
                'username': 'cliente_particular',
                'email': 'particular@email.com',
                'first_name': 'Pedro',
                'last_name': 'Particular',
                'password': 'particular123',
                'is_staff': False,
                'is_superuser': False,
                'tipo': 'Cliente Particular'
            }
        ]
        
        for user_data in usuarios_sistema:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=user_data['is_staff'],
                    is_superuser=user_data['is_superuser'],
                    is_active=True,
                    password=make_password(user_data['password'])
                )
                icono = "👔" if user_data['is_staff'] else "👤"
                self.stdout.write(f'✅ {icono} {user_data["tipo"]} creado: {user_data["username"]}')
            else:
                self.stdout.write(f'→ Usuario ya existe: {user_data["username"]}')
        
        # Verificar usuario existente cliente_prueba
        if User.objects.filter(username='cliente_prueba').exists():
            self.stdout.write('→ Usuario cliente_prueba ya existe (mantener)')
        
        self.stdout.write('')
        self.stdout.write('🎉 ¡Sistema de usuarios de ferretería configurado!')
        self.stdout.write('')
        self.stdout.write('📋 CREDENCIALES DEL SISTEMA:')
        self.stdout.write('=' * 50)
        self.stdout.write(f'👑 SUPER ADMIN: {username} / {password}')
        self.stdout.write('👔 VENDEDOR: vendedor_ferreteria / vendedor123')
        self.stdout.write('👔 SUPERVISOR: supervisor_tienda / supervisor123')
        self.stdout.write('👤 EMPRESA: cliente_empresa / empresa123')
        self.stdout.write('👤 PARTICULAR: cliente_particular / particular123')
        self.stdout.write('👤 PRUEBA: cliente_prueba / ferramas123')
        self.stdout.write('')
        self.stdout.write('🚀 ACCESOS DISPONIBLES:')
        self.stdout.write('• Panel Admin: http://127.0.0.1:8000/admin-ferreteria/')
        self.stdout.write('• Admin Django: http://127.0.0.1:8000/admin/')
        self.stdout.write('• Tienda: http://127.0.0.1:8000/')
        self.stdout.write('• Login: http://127.0.0.1:8000/accounts/login/')