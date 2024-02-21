from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import Landing, Home, Login, logoutUsuario, ListarUsuario, RegistrarUsuario, EditarUsuario, EliminarUsuario, CambiarContraseña, CambiarContraseñaModal, CambiarPerfil, DesbloquearUsuario, ListarZona, EditarZona, RegistrarZona, EliminarZona, ListarRepresentante, EditarRepresentante, RegistrarRepresentante, EliminarRepresentante, ListarPaciente, EditarPaciente, RegistrarPaciente, EliminarPaciente, ListarUbicacion, EditarUbicacion, RegistrarUbicacion, EliminarUbicacion, ListarTipo_insumo, EditarTipo_insumo, RegistrarTipo_insumo, EliminarTipo_insumo, ListarLote, EditarLote, RegistrarLote, EliminarLote, ListarLaboratorio, EditarLaboratorio, RegistrarLaboratorio, EliminarLaboratorio, ListarProducto, EditarProducto, RegistrarProducto, EliminarProducto, ListarSolicitud, EditarSolicitud, RegistrarSolicitud, EliminarSolicitud, Solicitud, ListarEmpleado, EditarEmpleado, RegistrarEmpleado, EliminarEmpleado, ListarFactura, EditarFactura, RegistrarFactura, EliminarFactura, ListarTipo_mov, EditarTipo_mov, RegistrarTipo_mov, EliminarTipo_mov, ListarMovimiento_inventario, EditarMovimiento_inventario, RegistrarMovimiento_inventario, EliminarMovimiento_inventario
from . import views


urlpatterns = [

    #------------------------------ Landing ------------------------------#
    
    path('', Landing.as_view(), name="landing"),

    #------------------------------ Inicio ------------------------------#

    path('home/', login_required(Home.as_view()), name="home"),
    path('accounts/login/', Login.as_view(), name="login"),
    path('logout/', login_required(logoutUsuario), name='logout'),

    #------------------------------ Usuario ------------------------------#

    path('registrarUsuario/', login_required(RegistrarUsuario.as_view()), name="registrar_Usuario"),
    path('inicioUsuario/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Usuario/listarUsuario.html'
                                    )
                                ), name="inicio_Usuario"),
    path('listarUsuario/', login_required(ListarUsuario.as_view()), name="listar_Usuario"),
    path('editarUsuario/<int:pk>/', login_required(EditarUsuario.as_view()), name="editar_Usuario"),
    path('eliminarUsuario/<int:pk>/', login_required(EliminarUsuario.as_view()), name="eliminar_Usuario"),
    path('cambiarMiContraseña/<int:pk>/', login_required(CambiarContraseña.as_view()), name="cambiar_Mi_Contraseña"),
    path('cambiarContraseña/<int:pk>/', login_required(CambiarContraseñaModal.as_view()), name="cambiar_Contraseña"),
    path('cambiarPerfil/<int:pk>/', login_required(CambiarPerfil.as_view()), name="cambiar_Perfil"),
    path('desbloquearUsuario/<int:pk>/', login_required(DesbloquearUsuario.as_view()), name="desbloquear_Usuario"),
    
    #------------------------------ Zona ------------------------------#

    path('registrarZona/', login_required(RegistrarZona.as_view()), name="registrar_Zona"),
    path('inicioZona/', login_required(
    							TemplateView.as_view(
    								template_name = 'Zona/listarZona.html'
    								)
    							), name="inicio_Zona"),
    path('listarZona/', login_required(ListarZona.as_view()), name="listar_Zona"),
    path('editarZona/<int:pk>/', login_required(EditarZona.as_view()), name="editar_Zona"),
    path('eliminarZona/<int:pk>/', login_required(EliminarZona.as_view()), name="eliminar_Zona"),

    #------------------------------ Representante ------------------------------#

    path('registrarRepresentante/', login_required(RegistrarRepresentante.as_view()), name="registrar_Representante"),
    path('inicioRepresentante/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Representante/listarRepresentante.html'
                                    )
                                ), name="inicio_Representante"),
    path('listarRepresentante/', login_required(ListarRepresentante.as_view()), name="listar_Representante"),
    path('editarRepresentante/<int:pk>/', login_required(EditarRepresentante.as_view()), name="editar_Representante"),
    path('eliminarRepresentante/<int:pk>/', login_required(EliminarRepresentante.as_view()), name="eliminar_Representante"),

    #------------------------------ Paciente ------------------------------#

    path('registrarPaciente/', login_required(RegistrarPaciente.as_view()), name="registrar_Paciente"),
    path('inicioPaciente/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Paciente/listarPaciente.html'
                                    )
                                ), name="inicio_Paciente"),
    path('listarPaciente/', login_required(ListarPaciente.as_view()), name="listar_Paciente"),
    path('editarPaciente/<int:pk>/', login_required(EditarPaciente.as_view()), name="editar_Paciente"),
    path('eliminarPaciente/<int:pk>/', login_required(EliminarPaciente.as_view()), name="eliminar_Paciente"),

    #------------------------------ Ubicacion ------------------------------#

    path('registrarUbicacion/', login_required(RegistrarUbicacion.as_view()), name="registrar_Ubicacion"),
    path('inicioUbicacion/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Ubicacion/listarUbicacion.html'
                                    )
                                ), name="inicio_Ubicacion"),
    path('listarUbicacion/', login_required(ListarUbicacion.as_view()), name="listar_Ubicacion"),
    path('editarUbicacion/<int:pk>/', login_required(EditarUbicacion.as_view()), name="editar_Ubicacion"),
    path('eliminarUbicacion/<int:pk>/', login_required(EliminarUbicacion.as_view()), name="eliminar_Ubicacion"),

    #------------------------------ Tipo de Insumo ------------------------------#

    path('registrarTipo_insumo/', login_required(RegistrarTipo_insumo.as_view()), name="registrar_Tipo_insumo"),
    path('inicioTipo_insumo/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Tipo_insumo/listarTipo_insumo.html'
                                    )
                                ), name="inicio_Tipo_insumo"),
    path('listarTipo_insumo/', login_required(ListarTipo_insumo.as_view()),  name="listar_Tipo_insumo"),
    path('editarTipo_insumo/<int:pk>/', login_required(EditarTipo_insumo.as_view()), name="editar_Tipo_insumo"),
    path('eliminarTipo_insumo/<int:pk>/', login_required(EliminarTipo_insumo.as_view()), name="eliminar_Tipo_insumo"),

    #------------------------------ Lote ------------------------------#

    path('registrarLote/', login_required(RegistrarLote.as_view()), name="registrar_Lote"),
    path('inicioLote/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Lote/listarLote.html'
                                    )
                                ), name="inicio_Lote"),
    path('listarLote/', login_required(ListarLote.as_view()), name="listar_Lote"),
    path('editarLote/<int:pk>/', login_required(EditarLote.as_view()), name="editar_Lote"),
    path('eliminarLote/<int:pk>/', login_required(EliminarLote.as_view()), name="eliminar_Lote"),

    #------------------------------ Laboratorio ------------------------------#

    path('registrarLaboratorio/', login_required(RegistrarLaboratorio.as_view()), name="registrar_Laboratorio"),
    path('inicioLaboratorio/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Laboratorio/listarLaboratorio.html'
                                    )
                                ), name="inicio_Laboratorio"),
    path('listarLaboratorio/', login_required(ListarLaboratorio.as_view()), name="listar_Laboratorio"),
    path('editarLaboratorio/<int:pk>/', login_required(EditarLaboratorio.as_view()), name="editar_Laboratorio"),
    path('eliminarLaboratorio/<int:pk>/', login_required(EliminarLaboratorio.as_view()), name="eliminar_Laboratorio"),

    #------------------------------ Producto ------------------------------#

    path('registrarProducto/',login_required(RegistrarProducto.as_view()), name="registrar_Producto"),
    path('inicioProducto/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Producto/listarProducto.html'
                                    )
                                ), name="inicio_Producto"),
    path('listarProducto/', login_required(ListarProducto.as_view()), name="listar_Producto"),
    path('editarProducto/<int:pk>/', login_required(EditarProducto.as_view()), name="editar_Producto"),
    path('eliminarProducto/<int:pk>/', login_required(EliminarProducto.as_view()), name="eliminar_Producto"),

    #------------------------------ Solicitud de Medicamento ------------------------------#

    path('registrarSolicitud/',login_required(RegistrarSolicitud.as_view()), name="registrar_Solicitud"),
    path('inicioSolicitud/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Solicitud/listarSolicitud.html'
                                    )
                                ), name="inicio_Solicitud"),
    path('listarSolicitud/', login_required(ListarSolicitud.as_view()), name="listar_Solicitud"),
    path('editarSolicitud/<int:pk>/', login_required(EditarSolicitud.as_view()), name="editar_Solicitud"),
    path('eliminarSolicitud/<int:pk>/', login_required(EliminarSolicitud.as_view()), name="eliminar_Solicitud"),
    path('solicitud/', login_required(Solicitud.as_view()), name="solicitud"),

    #------------------------------ Empleado ------------------------------#

    path('registrarEmpleado/',login_required(RegistrarEmpleado.as_view()), name="registrar_Empleado"),
    path('inicioEmpleado/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Empleado/listarEmpleado.html'
                                    )
                                ), name="inicio_Empleado"),
    path('listarEmpleado/', login_required(ListarEmpleado.as_view()), name="listar_Empleado"),
    path('editarEmpleado/<int:pk>/', login_required(EditarEmpleado.as_view()), name="editar_Empleado"),
    path('eliminarEmpleado/<int:pk>/', login_required(EliminarEmpleado.as_view()), name="eliminar_Empleado"),
    
    #------------------------------ Factura ------------------------------#

    path('registrarFactura/',login_required(RegistrarFactura.as_view()), name="registrar_Factura"),
    path('inicioFactura/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Factura/listarFactura.html'
                                    )
                                ), name="inicio_Factura"),
    path('listarFactura/', login_required(ListarFactura.as_view()), name="listar_Factura"),
    path('editarFactura/<int:pk>/', login_required(EditarFactura.as_view()), name="editar_Factura"),
    path('eliminarFactura/<int:pk>/', login_required(EliminarFactura.as_view()), name="eliminar_Factura"),

    #------------------------------ Tipo de Movimiento ------------------------------#

    path('registrarTipo_mov/',login_required(RegistrarTipo_mov.as_view()), name="registrar_Tipo_mov"),
    path('inicioTipo_mov/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Tipo_mov/listarTipo_mov.html'
                                    )
                                ), name="inicio_Tipo_mov"),
    path('listarTipo_mov/', login_required(ListarTipo_mov.as_view()), name="listar_Tipo_mov"),
    path('editarTipo_mov/<int:pk>/', login_required(EditarTipo_mov.as_view()), name="editar_Tipo_mov"),
    path('eliminarTipo_mov/<int:pk>/', login_required(EliminarTipo_mov.as_view()), name="eliminar_Tipo_mov"),

    #------------------------------ Movimiento de Inventario ------------------------------#

    path('registrarMovimiento_inventario/',login_required(RegistrarMovimiento_inventario.as_view()), name="registrar_Movimiento_inventario"),
    path('inicioMovimiento_inventario/', login_required(
                                TemplateView.as_view(
                                    template_name = 'Movimiento_inventario/listarMovimiento_inventario.html'
                                    )
                                ), name="inicio_Movimiento_inventario"),
    path('listarMovimiento_inventario/', login_required(ListarMovimiento_inventario.as_view()), name="listar_Movimiento_inventario"),
    path('editarMovimiento_inventario/<int:pk>/', login_required(EditarMovimiento_inventario.as_view()), name="editar_Movimiento_inventario"),
    path('eliminarMovimiento_inventario/<int:pk>/', login_required(EliminarMovimiento_inventario.as_view()), name="eliminar_Movimiento_inventario"),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)