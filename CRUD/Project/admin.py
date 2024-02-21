from django.contrib import admin
from .models import Usuario, Zona, Representante, Paciente, Ubicacion, Tipo_insumo, Lote, Laboratorio, Producto, Solicitud, Empleado, Factura, Tipo_mov, Movimiento_inventario

# Register your models here.

@admin.register(Usuario)
class Usuario(admin.ModelAdmin):
	list_display = ('cod_usuario', 'username', 'nombre', 'apellido', 'email', 'imagen', 'intentos_fallidos', 'cuenta_bloqueada', 'paciente')

@admin.register(Zona)
class Zona(admin.ModelAdmin):
	list_display = ('id_zona', 'zona_residencia')

@admin.register(Representante)
class Representante(admin.ModelAdmin):
	list_display = ('cod_repr', 'tipo_cedula_repr', 'cedula_repr', 'nombre_repr', 'apellido_repr', 'parentesco')

@admin.register(Paciente)
class Paciente(admin.ModelAdmin):
	list_display = ('cod_pac', 'tipo_cedula_pac', 'cedula_pac', 'nombre_pac', 'apellido_pac', 'tipo_telefono_pac', 'telefono_pac', 'id_zona', 'sexo_pac', 'fecha_nacimiento_pac', 'embarazada', 'cod_repr', 'constancia_residencia',)

@admin.register(Ubicacion)
class Ubicacion(admin.ModelAdmin):
	list_display = ('id_zona', 'ubicacion')

@admin.register(Tipo_insumo)
class Tipo_insumo(admin.ModelAdmin):
	list_display = ('id_tipo_insumo', 'nombre_tipo_insumo')

@admin.register(Lote)
class Lote(admin.ModelAdmin):
	list_display = ('id_lote', 'lote', 'canti_pro', 'fecha_lote')

@admin.register(Laboratorio)
class Laboratorio(admin.ModelAdmin):
	list_display = ('id_laboratorio', 'nombre_laboratorio')

@admin.register(Producto)
class Producto(admin.ModelAdmin):
	list_display = ('id_producto', 'nombre_producto', 'id_ubicacion', 'id_tipo_insumo', 'id_lote', 'id_laboratorio', 'limite', 'stock_max', 'stock_min')

@admin.register(Solicitud)
class Solicitud(admin.ModelAdmin):
	list_display = ('id_soli', 'fecha_soli', 'descripcion_soli', 'cantidad')

@admin.register(Empleado)
class Empleado(admin.ModelAdmin):
	list_display = ('cod_empl', 'tipo_cedula_empl', 'cedula_empl', 'nombre_empl', 'apellido_empl', 'tipo_telefono_empl', 'telefono_empl', 'direccion_exacta', 'cargo')

@admin.register(Factura)
class Factura(admin.ModelAdmin):
	list_display = ('cod_fac', 'fecha_fac', 'cod_pac', 'cod_empl', 'descripcion', 'id_producto', 'cantidad')

@admin.register(Tipo_mov)
class Tipo_mov(admin.ModelAdmin):
	list_display = ('tipo_mov', 'descripcion')

@admin.register(Movimiento_inventario)
class Movimiento_inventario(admin.ModelAdmin):
	list_display = ('id_mov', 'fecha_mov', 'motivo_mov', 'tipo_mov', 'cod_empl', 'id_producto', 'cantidad')
