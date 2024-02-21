import json
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import IntegrityError
from django.forms.widgets import HiddenInput
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import forms
from .forms import FormularioLogin, FormularioUsuario, FormularioUsuarioEdicion, ZonaForm, RepresentanteForm, PacienteForm, UbicacionForm, Tipo_insumoForm, LoteForm, LaboratorioForm, ProductoForm, SolicitudForm, SolicitudEdicionForm, EmpleadoForm, FacturaForm, Tipo_movForm, Movimiento_inventarioForm
from .models import Usuario, Zona, Representante, Paciente, Ubicacion, Tipo_insumo, Lote, Laboratorio, Producto, Solicitud, Empleado, Factura, Tipo_mov, Movimiento_inventario
from django.contrib.admin.views.decorators import staff_member_required
from io import BytesIO
from datetime import date
from django.core.management import call_command
from django.conf import settings
import datetime
from django.contrib import messages


# Create your views here.
#------------------------------ Landing ------------------------------#

class Landing(TemplateView):
    template_name = 'Landingpage/landing.html'

#------------------------------ INICIO ------------------------------#


class Home(TemplateView):
    template_name = 'Inicio/index.html'

#------------------------------ LOGIN y LOGAUT ------------------------------#


class Login(FormView):
    template_name = 'Inicio/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if user.cuenta_bloqueada:
            messages.error(self.request, 'Cuenta bloqueada. Por favor, contacte al administrador.')
            return self.form_invalid(form)

        login(self.request, user)
        # Reiniciar los intentos fallidos al iniciar sesión exitosamente
        user.intentos_fallidos = 0
        user.save()

        return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')

        try:
            user = Usuario.objects.get(username=username)
            user.intentos_fallidos += 1

            if user.intentos_fallidos >= 3:
                user.cuenta_bloqueada = True
                user.save()
                messages.error(self.request, 'Cuenta bloqueada. Por favor, contacte al administrador.')
            else:
                user.save()
                messages.error(self.request, 'Contraseña incorrecta.')

        except Usuario.DoesNotExist:
            messages.error(self.request, 'Usuario no encontrado. Por favor, verifique el nombre de usuario.')

        return super(Login, self).form_invalid(form)


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


#------------------------------ USUARIO ------------------------------#


class ListarUsuario(View):
    model = Usuario

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            filtro_cargo = request.GET.get('cargo', None)
            
            if filtro_cargo:
                queryset = self.model.objects.filter(cargo=filtro_cargo)
            else:
                queryset = self.get_queryset()

            return HttpResponse(serialize('json', queryset), 'application/json')
        else:
            return redirect('inicio_Usuario')


class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuario/registrarUsuario.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_usuario = Usuario(
                    email = form.cleaned_data.get('email'),
                    username = form.cleaned_data.get('username'),
                    nombre = form.cleaned_data.get('nombre'),
                    apellido = form.cleaned_data.get('apellido'),
                    cargo = form.cleaned_data.get('cargo')
                )
                nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                nuevo_usuario.save()
                mensaje = f'El Usuario se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Usuario no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Usuario')


class EditarUsuario(UpdateView):
    model = Usuario
    form_class = FormularioUsuarioEdicion
    template_name = 'Usuario/editarUsuario.html'
    context_object_name = 'usuario'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Usuario se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Usuario no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Usuario')


class EliminarUsuario(DeleteView):
    model = Usuario
    template_name = 'Usuario/eliminarUsuario.html'
    success_url = reverse_lazy('inicio_Usuario')
    context_object_name = 'usuario'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            usuario = self.get_object()
            form.delete()
            mensaje = f'El Usuario se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Usuario')
            
class CambiarContraseña(UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Inicio/cambiarContraseña.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['cargo'].widget = forms.HiddenInput()
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Contraseña se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Contraseña no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('login')

class CambiarContraseñaModal(UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'Usuario/cambiarContraseña.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['cargo'].widget = forms.HiddenInput()
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, request.FILES, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Contraseña se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Contraseña no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Usuario')

class CambiarPerfil(UpdateView):
    model = Usuario
    form_class = FormularioUsuarioEdicion
    template_name = 'Inicio/cambiarPerfil.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['cargo'].widget = forms.HiddenInput()
        form.fields['intentos_fallidos'].widget = forms.HiddenInput()
        form.fields['cuenta_bloqueada'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            mensaje = 'El perfil se ha actualizado correctamente'
            error = 'No hay error'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                messages.success(request, mensaje)
                return redirect('home')
        else:
            mensaje = 'El perfil no se ha podido actualizar'
            error = form.errors
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
            else:
                messages.error(request, mensaje)
                return redirect('home')

class DesbloquearUsuario(UpdateView):
    model = Usuario
    form_class = FormularioUsuarioEdicion
    template_name = 'Usuario/desbloquearUsuario.html'
    context_object_name = 'usuario'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].widget = forms.HiddenInput()
        form.fields['username'].widget = forms.HiddenInput()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['apellido'].widget = forms.HiddenInput()
        form.fields['cargo'].widget = forms.HiddenInput()
        form.fields['imagen'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            mensaje = 'El Usuario ha sido desbloqueado correctamente'
            error = 'No hay error'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                messages.success(request, mensaje)
                return redirect('inicio_Usuario')
        else:
            mensaje = 'El Usuario no se ha podido desbloquear'
            error = form.errors
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
            else:
                messages.error(request, mensaje)
                return redirect('inicio_Usuario')

#------------------------------ Zona ------------------------------#


class ListarZona(View):
    model = Zona

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Zona')

class EditarZona(UpdateView):
    model = Zona
    form_class = ZonaForm
    template_name = 'Zona/editarZona.html'
    context_object_name = 'zona'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Zona se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Zona no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Zona')

class RegistrarZona(CreateView):
    model = Zona
    form_class = ZonaForm
    template_name = 'Zona/registrarZona.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'La Zona se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Zona no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Zona')

class EliminarZona(DeleteView):
    model = Zona
    template_name = 'Zona/eliminarZona.html'
    success_url = reverse_lazy('inicio_Zona')
    context_object_name = 'zona'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            zona = self.get_object()
            form.delete()
            mensaje = f'La Zona se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Zona')


#------------------------------ Representante ------------------------------#


class ListarRepresentante(View):
    model = Representante

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Representante')

class EditarRepresentante(UpdateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'Representante/editarRepresentante.html'
    context_object_name = 'representante'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo_cedula_repr'].widget = forms.HiddenInput()
        form.fields['cedula_repr'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Representante se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Representante no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Representante')

class RegistrarRepresentante(CreateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'Representante/registrarRepresentante.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Representante se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Representante no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Representante')

class EliminarRepresentante(DeleteView):
    model = Representante
    template_name = 'Representante/eliminarRepresentante.html'
    success_url = reverse_lazy('inicio_Representante')
    context_object_name = 'representante'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            representante = self.get_object()
            form.delete()
            mensaje = f'El Representante se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Representante')


#------------------------------ Paciente ------------------------------#


class ListarPaciente(View):
    model = Paciente

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Paciente')

class EditarPaciente(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'Paciente/editarPaciente.html'
    context_object_name = 'paciente'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo_cedula_pac'].widget = forms.HiddenInput()
        form.fields['cedula_pac'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, request.FILES ,instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Paciente se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Paciente no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Paciente')

class RegistrarPaciente(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'Paciente/registrarPaciente.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                mensaje = f'El Paciente se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Paciente no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Paciente')

class EliminarPaciente(DeleteView):
    model = Paciente
    template_name = 'Paciente/eliminarPaciente.html'
    success_url = reverse_lazy('inicio_Paciente')
    context_object_name = 'paciente'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            paciente = self.get_object()
            form.delete()
            mensaje = f'El Paciente se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Paciente')


#------------------------------ Ubicación ------------------------------#


class ListarUbicacion(View):
    model = Ubicacion

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Ubicacion')

class EditarUbicacion(UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'Ubicacion/editarUbicacion.html'
    context_object_name = 'ubicacion'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'La Ubicacion se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Ubicacion no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Ubicacion')

class RegistrarUbicacion(CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'Ubicacion/registrarUbicacion.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'La Ubicacion se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La Ubicacion no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Ubicacion')

class EliminarUbicacion(DeleteView):
    model = Ubicacion
    template_name = 'Ubicacion/eliminarUbicacion.html'
    success_url = reverse_lazy('inicio_Ubicacion')
    context_object_name = 'ubicacion'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            ubicacion = self.get_object()
            form.delete()
            mensaje = f'La Ubicacion se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Ubicacion')


#------------------------------ Tipo_insumo ------------------------------#


class ListarTipo_insumo(View):
    model = Tipo_insumo

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Tipo_insumo')

class EditarTipo_insumo(UpdateView):
    model = Tipo_insumo
    form_class = Tipo_insumoForm
    template_name = 'Tipo_insumo/editarTipo_insumo.html'
    context_object_name = 'tipo_insumo'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El tipo de insumo se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Tipo de insumo no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Tipo_insumo')

class RegistrarTipo_insumo(CreateView):
    model = Tipo_insumo
    form_class = Tipo_insumoForm
    template_name = 'Tipo_insumo/registrarTipo_insumo.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Tipo de insumo se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Tipo de insumo no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Tipo_insumo')

class EliminarTipo_insumo(DeleteView):
    model = Tipo_insumo
    template_name = 'Tipo_insumo/eliminarTipo_insumo.html'
    success_url = reverse_lazy('inicio_Tipo_insumo')
    context_object_name = 'tipo_insumo'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            tipo_insumo = self.get_object()
            form.delete()
            mensaje = f'El Tipo de insumo se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Tipo_insumo')


#------------------------------ Lote ------------------------------#


class ListarLote(View):
    model = Lote

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Lote')

class EditarLote(UpdateView):
    model = Lote
    form_class = LoteForm
    template_name = 'Lote/editarLote.html'
    context_object_name = 'lote'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Lote se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Lote no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Lote')

class RegistrarLote(CreateView):
    model = Lote
    form_class = LoteForm
    template_name = 'Lote/registrarLote.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Lote se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Lote no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Lote')

class EliminarLote(DeleteView):
    model = Lote
    template_name = 'Lote/eliminarLote.html'
    success_url = reverse_lazy('inicio_Lote')
    context_object_name = 'lote'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            lote = self.get_object()
            form.delete()
            mensaje = f'El Lote se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Lote')


#------------------------------ Laboratorio ------------------------------#


class ListarLaboratorio(View):
    model = Laboratorio

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Laboratorio')

class EditarLaboratorio(UpdateView):
    model = Laboratorio
    form_class = LaboratorioForm
    template_name = 'Laboratorio/editarLaboratorio.html'
    context_object_name = 'laboratorio'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Laboratorio se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Laboratorio no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Laboratorio')

class RegistrarLaboratorio(CreateView):
    model = Laboratorio
    form_class = LaboratorioForm
    template_name = 'Laboratorio/registrarLaboratorio.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Laboratorio se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Laboratorio no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Laboratorio')

class EliminarLaboratorio(DeleteView):
    model = Laboratorio
    template_name = 'Laboratorio/eliminarLaboratorio.html'
    success_url = reverse_lazy('inicio_Laboratorio')
    context_object_name = 'laboratorio'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            laboratorio = self.get_object()
            form.delete()
            mensaje = f'El Laboratorio se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Laboratorio')


#------------------------------ Producto ------------------------------#


class ListarProducto(View):
    model = Producto

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Producto')

class EditarProducto(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'Producto/editarProducto.html'
    context_object_name = 'producto'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Producto se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Producto no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Producto')

class RegistrarProducto(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'Producto/registrarProducto.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Producto se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Producto no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Producto')

class EliminarProducto(DeleteView):
    model = Producto
    template_name = 'Producto/eliminarProducto.html'
    success_url = reverse_lazy('inicio_Producto')
    context_object_name = 'producto'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            producto = self.get_object()
            form.delete()
            mensaje = f'El Producto se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Producto')


#------------------------------ Solicitud ------------------------------#


class ListarSolicitud(View):
    model = Solicitud

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Solicitud')

class EditarSolicitud(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'Solicitud/editarSolicitud.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            solicitud = self.get_object()
            form = self.form_class(request.POST, request.FILES, instance=solicitud)
            if form.is_valid():
                solicitud = form.save(commit=False)
                # Asignar el usuario actual o cualquier otro dato que necesites
                solicitud.user = request.user
                solicitud.save()
                form.save_m2m()  # Guardar las relaciones ManyToMany
                mensaje = f'El Solicitud se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Solicitud no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Solicitud')

class RegistrarSolicitud(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'Solicitud/registrarSolicitud.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                solicitud = form.save(commit=False)
                # Asignar el usuario actual o cualquier otro dato que necesites
                solicitud.user = request.user
                solicitud.save()
                form.save_m2m()  # Guardar las relaciones ManyToMany
                mensaje = f'El Solicitud se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Solicitud no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Solicitud')

class EliminarSolicitud(DeleteView):
    model = Solicitud
    template_name = 'Solicitud/eliminarSolicitud.html'
    success_url = reverse_lazy('inicio_Solicitud')
    context_object_name = 'solicitud'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            solicitud = self.get_object()
            form.delete()
            mensaje = f'El Solicitud se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Solicitud')


class Solicitud(CreateView):
    model = Solicitud
    form_class = SolicitudEdicionForm
    template_name = 'Inicio/solicitud.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                solicitud = form.save(commit=False)
                # Obtener el paciente relacionado con el usuario activo
                paciente = request.user.paciente
                solicitud.cod_pac = paciente
                solicitud.save()
                form.save_m2m()  # Guardar las relaciones ManyToMany
                mensaje = f'La solicitud se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'La solicitud no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Solicitud')


#------------------------------ Empleado ------------------------------#


class ListarEmpleado(View):
    model = Empleado

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            filtro_cargo = request.GET.get('cargo', None)
            
            if filtro_cargo:
                queryset = self.model.objects.filter(cargo=filtro_cargo)
            else:
                queryset = self.get_queryset()

            return HttpResponse(serialize('json', queryset), 'application/json')
        else:
            return redirect('inicio_Empleado')

class EditarEmpleado(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/editarEmpleado.html'
    context_object_name = 'empleado'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo_cedula_empl'].widget = forms.HiddenInput()
        form.fields['cedula_empl'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Empleado se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Empleado no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Empleado')

class RegistrarEmpleado(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/registrarEmpleado.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Empleado se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Empleado no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Empleado')

class EliminarEmpleado(DeleteView):
    model = Empleado
    template_name = 'Empleado/eliminarEmpleado.html'
    success_url = reverse_lazy('inicio_Empleado')
    context_object_name = 'empleado'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            empleado = self.get_object()
            form.delete()
            mensaje = f'El Empleado se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Empleado')


#------------------------------ Factura ------------------------------#


class ListarFactura(View):
    model = Factura

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Factura')

class EditarFactura(UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'Factura/editarFactura.html'
    context_object_name = 'factura'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Factura se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Factura no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Factura')

class RegistrarFactura(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'Factura/registrarFactura.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Tipo de Movimiento se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Tipo de Movimiento no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Factura')

class EliminarFactura(DeleteView):
    model = Factura
    template_name = 'Factura/eliminarFactura.html'
    success_url = reverse_lazy('inicio_Factura')
    context_object_name = 'factura'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            empleado = self.get_object()
            form.delete()
            mensaje = f'El Tipo de Movimiento se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Factura')


#------------------------------ Tipo de Movimiento ------------------------------#


class ListarTipo_mov(View):
    model = Tipo_mov

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Tipo_mov')

class EditarTipo_mov(UpdateView):
    model = Tipo_mov
    form_class = Tipo_movForm
    template_name = 'Tipo_mov/editarTipo_mov.html'
    context_object_name = 'tipo_mov'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Tipo de Movimiento se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Tipo de Movimiento no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Tipo_mov')

class RegistrarTipo_mov(CreateView):
    model = Tipo_mov
    form_class = Tipo_movForm
    template_name = 'Tipo_mov/registrarTipo_mov.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Tipo de Movimiento se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Tipo de Movimiento no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Tipo_mov')

class EliminarTipo_mov(DeleteView):
    model = Tipo_mov
    template_name = 'Tipo_mov/eliminarTipo_mov.html'
    success_url = reverse_lazy('inicio_Tipo_mov')
    context_object_name = 'tipo_mov'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            empleado = self.get_object()
            form.delete()
            mensaje = f'El Tipo de Movimiento se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Tipo_mov')


#------------------------------ Movimiento de Inventario ------------------------------#


class ListarMovimiento_inventario(View):
    model = Movimiento_inventario

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(serialize('json', self.get_queryset()), 'application/json')
        else:
            return redirect('inicio_Movimiento_inventario')

class EditarMovimiento_inventario(UpdateView):
    model = Movimiento_inventario
    form_class = Movimiento_inventarioForm
    template_name = 'Movimiento_inventario/editarMovimiento_inventario.html'
    context_object_name = 'movimiento_inventario'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'El Movimiento se ha actualizado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Movimiento no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Movimiento_inventario')

class RegistrarMovimiento_inventario(CreateView):
    model = Movimiento_inventario
    form_class = Movimiento_inventarioForm
    template_name = 'Movimiento_inventario/registrarMovimiento_inventario.html'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                mensaje = f'El Movimiento se ha registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 201
                return response
            else:
                mensaje = f'El Movimiento no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
        else:
            return redirect('inicio_Movimiento_inventario')

class EliminarMovimiento_inventario(DeleteView):
    model = Movimiento_inventario
    template_name = 'Movimiento_inventario/eliminarMovimiento_inventario.html'
    success_url = reverse_lazy('inicio_Movimiento_inventario')
    context_object_name = 'movimiento_inventario'

    def delete(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            empleado = self.get_object()
            form.delete()
            mensaje = f'El Movimiento se ha eliminado correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        else:
            return redirect('inicio_Movimiento_inventario')