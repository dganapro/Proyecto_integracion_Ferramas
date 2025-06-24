"""
Comando de Django para poblar la base de datos con datos de muestra para la ferretería
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalogo.models import Categoria, CarritoCompras, CarritoItem
from decimal import Decimal

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de muestra para la ferretería'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de muestra para Ferretería Ferramas...')
        
        # Crear categorías
        categorias_data = [
            {'nombre': 'Herramientas', 'descripcion': 'Herramientas manuales y eléctricas'},
            {'nombre': 'Fijaciones', 'descripcion': 'Clavos, tornillos, pernos y accesorios'},
            {'nombre': 'Pinturas', 'descripcion': 'Pinturas, barnices y productos relacionados'},
            {'nombre': 'Plomería', 'descripcion': 'Tuberías, grifos y accesorios de plomería'},
            {'nombre': 'Electricidad', 'descripcion': 'Cables, interruptores y material eléctrico'},
            {'nombre': 'Construcción', 'descripcion': 'Materiales de construcción y albañilería'},
        ]
        
        categorias_creadas = []
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categorias_creadas.append(categoria)
            if created:
                self.stdout.write(f'✓ Categoría creada: {categoria.nombre}')
            else:
                self.stdout.write(f'→ Categoría ya existe: {categoria.nombre}')
        
        # Crear usuario de prueba si no existe
        user, created = User.objects.get_or_create(
            username='cliente_prueba',
            defaults={
                'email': 'cliente@ferramas.com',
                'first_name': 'Cliente',
                'last_name': 'Prueba'
            }
        )
        if created:
            user.set_password('ferramas123')
            user.save()
            self.stdout.write('✓ Usuario de prueba creado: cliente_prueba / ferramas123')
        else:
            self.stdout.write('→ Usuario de prueba ya existe: cliente_prueba')
        
        # Crear carrito de muestra - ELIMINAR activo=True
        carrito, created = CarritoCompras.objects.get_or_create(
            usuario=user
            # Eliminar: activo=True (este campo no existe)
        )
        
        if created:
            # Agregar algunos items al carrito
            items_muestra = [
                {'producto_id': 1, 'nombre': 'Martillo 16oz', 'precio': Decimal('25000'), 'cantidad': 2},
                {'producto_id': 2, 'nombre': 'Destornillador Phillips', 'precio': Decimal('12000'), 'cantidad': 1},
                {'producto_id': 3, 'nombre': 'Clavos 2 pulgadas (1kg)', 'precio': Decimal('5000'), 'cantidad': 5},
            ]
            
            for item_data in items_muestra:
                CarritoItem.objects.create(
                    carrito=carrito,
                    producto_id=item_data['producto_id'],
                    producto_codigo=f"PROD{item_data['producto_id']:03d}",
                    producto_nombre=item_data['nombre'],
                    precio_unitario=item_data['precio'],
                    cantidad=item_data['cantidad']
                )
            
            self.stdout.write('✓ Carrito de muestra creado con productos')
        else:
            self.stdout.write('→ Carrito de muestra ya existe')
        
        self.stdout.write(
            self.style.SUCCESS('🎉 ¡Datos de muestra creados exitosamente!')
        )
        
        # Mostrar resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write('📊 RESUMEN DE DATOS CREADOS:')
        self.stdout.write(f'✓ Categorías: {len(categorias_creadas)}')
        self.stdout.write(f'✓ Usuario de prueba: cliente_prueba')
        self.stdout.write(f'✓ Carrito con {len(items_muestra) if created else "productos existentes"}')
        self.stdout.write('='*50)
        
        self.stdout.write('\n🚀 Para iniciar el sistema:')
        self.stdout.write('1. python manage.py runserver')
        self.stdout.write('2. Ir a http://127.0.0.1:8000')
        self.stdout.write('3. Login: cliente_prueba / ferramas123')