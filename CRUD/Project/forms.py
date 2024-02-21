from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Zona, Representante, Paciente, Ubicacion, Tipo_insumo, Lote, Laboratorio, Producto, Solicitud, Empleado, Factura, Tipo_mov, Movimiento_inventario

class UploadFileForm(forms.Form):
    file = forms.FileField()
    
class FormularioLogin(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(FormularioLogin, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
		self.fields['password'].widget.attrs['class'] = 'form-control'
		self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class FormularioUsuario(forms.ModelForm):
	imagen = forms.ImageField(required=False)

	password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Ingrese su contraseña',
			'id': 'password1',
			'required': 'required',
			}
		)
	)


	password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
		attrs = {
			'class': 'form-control',
			'placeholder': 'Ingrese nuevamente su contraseña',
			'id': 'password2',
			'required': 'required',
			}
		)
	)

	class Meta:
		model = Usuario
		fields = ('email', 'username', 'nombre', 'apellido', 'cargo')
		widgets = {
			'email': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico',
				}
			),
			'nombre': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre',

				}
			),
			'apellido': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido',
				}
			),
			'username': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre de usuario',
				}
			),
			'cargo': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('ADMINISTRADOR', 'ADMINISTRADOR'), ('ALMACENISTA', 'ALMACENISTA'), ('ATENCION AL CLIENTE', 'ATENCION AL CLIENTE'), ('PACIENTE', 'PACIENTE'), ('JEFE DE COMUNIDAD', 'JEFE DE COMUNIDAD')],
				attrs = {
					'class': 'form-control'
				}
			)
		}

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError('Contraseñas no coinciden')
		return password2

	def save(self, commit = True):
		usuario = super().save(commit = False)
		usuario.set_password(self.cleaned_data['password1'])
		if commit:
			usuario.save()
		return usuario

class FormularioUsuarioEdicion(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ('email', 'username', 'nombre', 'apellido', 'cargo', 'imagen', 'intentos_fallidos', 'cuenta_bloqueada')
		widgets = {
			'email': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico',
				}
			),
			'nombre': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre',

				}
			),
			'apellido': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido',
				}
			),
			'username': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre de usuario',
				}
			),
			'cargo': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('ADMINISTRADOR', 'ADMINISTRADOR'), ('ALMACENISTA', 'ALMACENISTA'), ('ATENCION AL CLIENTE', 'ATENCION AL CLIENTE'), ('PACIENTE', 'PACIENTE'), ('JEFE DE COMUNIDAD', 'JEFE DE COMUNIDAD')],
				attrs = {
					'class': 'form-control'
				}
			)
		}

	def __init__(self, *args, **kwargs):
		super(FormularioUsuarioEdicion, self).__init__(*args, **kwargs)
		self.fields['imagen'].required = False
		self.fields['imagen'].widget.attrs['class'] = 'form-control'
		self.fields['intentos_fallidos'].required = False
		self.fields['intentos_fallidos'].widget.attrs['class'] = 'form-control'
		self.fields['cuenta_bloqueada'].required = False

	def save(self, commit=True):
		usuario = super().save(commit=False)
		if self.cleaned_data['imagen']:
			usuario.imagen = self.cleaned_data['imagen']
		if commit:
			usuario.save()
		return usuario


class ZonaForm(forms.ModelForm):
	class Meta:
		model = Zona
		fields = ['zona_residencia']
		label = {
			'zona_residencia': 'Zona',
		}
		widgets = {
			'zona_residencia': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Zona'
				}
			),
		}


class RepresentanteForm(forms.ModelForm):
	class Meta:
		model = Representante
		fields = ['tipo_cedula_repr','cedula_repr','nombre_repr', 'apellido_repr', 'parentesco']
		label = {
			'tipo_cedula_repr': '',
			'cedula_repr': 'Cedula',
			'nombre_repr': 'Nombre',
			'apellido_repr': 'Apellido',
			'parentesco': 'Parentesco',
		}
		widgets = {
			'tipo_cedula_repr': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('V-', 'V-'), ('E-', 'E-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'cedula_repr': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Cedula'
				}
			),
			'nombre_repr': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre'
				}
			),
			'apellido_repr': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido'
				}
			),
			'parentesco': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('MAMÁ', 'MAMÁ'), ('PAPÁ', 'PAPÁ'), ('ABUELA', 'ABUELA'), ('ABUELO', 'ABUELO'), ('TÍA', 'TÍA'), ('TÍO', 'TÍO'), ('HERMANO', 'HERMANO'), ('HERMANA', 'HERMANA'), ('PRIMO', 'PRIMO'), ('PRIMA', 'PRIMA')],
				attrs = {
					'class': 'form-control'
				}
			),
		}


class PacienteForm(forms.ModelForm):
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Ingrese su contraseña',
			'id': 'password1',
			'required': 'required',
		}
	))

	password2 = forms.CharField(label='Contraseña de confirmación', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Ingrese nuevamente su contraseña',
			'id': 'password2',
			'required': 'required',
		}
	))

	class Meta:
		model = Paciente
		fields = ['tipo_cedula_pac','cedula_pac','nombre_pac', 'apellido_pac', 'tipo_telefono_pac', 'telefono_pac', 'email_pac', 'cargo_pac', 'id_zona', 'sexo_pac', 'embarazada', 'fecha_nacimiento_pac', 'cod_repr', 'constancia_residencia', 'username_pac']
		label = {
			'tipo_cedula_pac': '',
			'cedula_pac': 'Cedula',
			'nombre_pac': 'Nombre',
			'apellido_pac': 'Apellido',
			'tipo_telefono_pac': '',
			'telefono_pac': 'Telefono',
			'email_pac': 'Correo electrónico',
			'cargo_pac': 'Cargo',
			'id_zona': 'Zona',
			'sexo_pac': 'Sexo',
			'embarazada': 'Embarazada',
			'fecha_nacimiento_pac': 'Fecha de nacimiento',
			'cod_repr': 'Cedula del representante',
			'constancia_residencia': 'Constancia de Residencia',
			'username_pac': 'Nombre de Usuario',
		}
		widgets = {
			'tipo_cedula_pac': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('V-', 'V-'), ('E-', 'E-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'cedula_pac': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Cedula'
				}
			),
			'nombre_pac': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre'
				}
			),
			'apellido_pac': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido'
				}
			),
			'tipo_telefono_pac': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('0412-', '0412-'), ('0414-', '0414-'), ('0416-', '0416-'), ('0424-', '0424-'), ('0426-', '0426-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'telefono_pac': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Telefono'
				}
			),
			'email_pac': forms.EmailInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Correo electrónico',
				}
			),
			'cargo_pac': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('PACIENTE', 'PACIENTE'), ('JEFE DE COMUNIDAD', 'JEFE DE COMUNIDAD')],
				attrs = {
					'class': 'form-control'
				}
			),
			'id_zona': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'sexo_pac': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('FEMENINO', 'FEMENINO'), ('MASCULINO', 'MASCULINO')],
				attrs = {
					'class': 'form-control'
				}
			),
			'embarazada': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('SI', 'SI'), ('NO', 'NO')],
				attrs = {
					'class': 'form-control'
				}
			),
			'fecha_nacimiento_pac': forms.DateInput(
				attrs = {
					'type': 'date',	
					'class': 'form-control'
				},
				format='%Y-%m-%d'
			),
			'cod_repr': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),	
			'username_pac': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre de usuario',
				}
			),
		}

	def __init__(self, *args, **kwargs):
		super(PacienteForm, self).__init__(*args, **kwargs)
		self.fields['constancia_residencia'].required = True
		self.fields['constancia_residencia'].widget.attrs['class'] = 'form-control'

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError('Las contraseñas no coinciden')
		return password2

	def save(self, commit=True):
		Paciente = super().save(commit=False)
		usuario = Usuario.objects.create_user(
			username=self.cleaned_data['username_pac'],
			email=self.cleaned_data['email_pac'],
			nombre=Paciente.nombre_pac,
			apellido=Paciente.apellido_pac,
			password=self.cleaned_data['password1'],
			cargo=Paciente.cargo_pac,
			paciente=Paciente.cod_pac
		)
		Paciente.username_pac = usuario.username
		if self.cleaned_data['constancia_residencia']:
			Paciente.constancia_residencia = self.cleaned_data['constancia_residencia']
		if commit:
			Paciente.save()
			usuario.paciente = Paciente
			usuario.save()
		return Paciente


class UbicacionForm(forms.ModelForm):
	class Meta:
		model = Ubicacion
		fields = ['ubicacion']
		label = {
			'ubicacion': 'Ubicación',
		}
		widgets = {
			'ubicacion': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Ubicación'
				}
			),
		}


class Tipo_insumoForm(forms.ModelForm):
	class Meta:
		model = Tipo_insumo
		fields = ['nombre_tipo_insumo']
		label = {
			'nombre_tipo_insumo': 'Tipo del Insumo',
		}
		widgets = {
			'nombre_tipo_insumo': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Tipo del Insumo'
				}
			),
		}


class LoteForm(forms.ModelForm):
	class Meta:
		model = Lote
		fields = ['lote', 'canti_pro']
		label = {
			'lote': 'Lote',
			'canti_pro': 'Cantidad del Producto'
		}
		widgets = {
			'lote': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Lote'
				}
			),
			'canti_pro': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad del Producto'
				}
			),
		}


class LaboratorioForm(forms.ModelForm):
	class Meta:
		model = Laboratorio
		fields = ['nombre_laboratorio']
		label = {
			'nombre_laboratorio': 'Laboratorio',
		}
		widgets = {
			'nombre_laboratorio': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Laboratorio'
				}
			),
		}


class ProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = ['nombre_producto', 'id_ubicacion', 'id_tipo_insumo', 'id_lote', 'id_laboratorio', 'limite', 'stock_max', 'stock_min']
		label = {
			'nombre_producto': 'Nombre del Producto',
			'id_ubicacion': 'Ubicación',
			'id_tipo_insumo': 'Tipo del insumo',
			'id_lote': 'Lote',
			'id_laboratorio': 'Laboratorio',
			'limite': 'Limite por paciente',
			'stock_max': 'Stock maximo',
			'stock_min': 'Stock minimo',
		}
		widgets = {
			'nombre_producto': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre del Producto'
				}
			),
			'existencial_inicial': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Existencia inicial'
				}
			),
			'existencial_actual': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Existencial actual'
				}
			),
			'id_ubicacion': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'id_tipo_insumo': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'id_laboratorio': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'id_lote': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'limite': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'limite por paciente'
				}
			),
			'stock_max': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Stock maximo'
				}
			),
			'stock_min': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Stock minimo'
				}
			),
		}


class SolicitudForm(forms.ModelForm):
	id_producto = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
	class Meta:
		model = Solicitud
		fields = ('cod_pac', 'descripcion_soli', 'id_producto', 'cantidad', 'recipe')
		label = {
			'cod_pac': 'Paciente',
			'descripcion_soli': 'Descripción de la Solicitud',
			'id_producto': 'Producto',
			'cantidad': 'Cantidad del Producto',
			'recipe':'Recipe',
		}
		widgets ={
			'cod_pac': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'descripcion_soli': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Descripcion de la Solicitud',
					'rows': '1'
				}
			),
			'cantidad': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad del Producto'
				}
			),
		}

	def __init__(self, *args, **kwargs):
		super(SolicitudForm, self).__init__(*args, **kwargs)
		self.fields['recipe'].required = True
		self.fields['recipe'].widget.attrs['class'] = 'form-control'

	def save(self, commit=True):
		Solicitud = super().save(commit=False)
		if self.cleaned_data['recipe']:
			Solicitud.recipe = self.cleaned_data['recipe']
		if commit:
			Solicitud.save()
		return Solicitud


class SolicitudEdicionForm(forms.ModelForm):
	id_producto = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
	class Meta:
		model = Solicitud
		fields = ('descripcion_soli', 'id_producto', 'cantidad', 'recipe')
		label = {
			'descripcion_soli': 'Descripción de la Solicitud',
			'id_producto': 'Producto',
			'cantidad': 'Cantidad del Producto',
			'recipe':'Recipe',
		}
		widgets ={
			'descripcion_soli': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Descripcion de la Solicitud',
					'rows': '1'
				}
			),
			'cantidad': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad del Producto'
				}
			),
		}

	def __init__(self, *args, **kwargs):
		super(SolicitudEdicionForm, self).__init__(*args, **kwargs)
		self.fields['recipe'].required = True
		self.fields['recipe'].widget.attrs['class'] = 'form-control'

	def save(self, commit=True):
		Solicitud = super().save(commit=False)
		if self.cleaned_data['recipe']:
			Solicitud.recipe = self.cleaned_data['recipe']
		if commit:
			Solicitud.save()
		return Solicitud


class EmpleadoForm(forms.ModelForm):
	class Meta:
		model = Empleado
		fields = ('tipo_cedula_empl', 'cedula_empl', 'nombre_empl', 'apellido_empl', 'tipo_telefono_empl', 'telefono_empl', 'direccion_exacta', 'cargo')
		label = {
			'tipo_cedula_empl': '',
			'cedula_empl': 'Cedula',
			'nombre_empl': 'Nombre',
			'apellido_empl': 'Apellido',
			'tipo_telefono_empl': '',
			'telefono_empl': 'Telefono movil',
			'direccion_exacta': 'Dirección',
			'cargo': 'Cargo',
		}
		widgets = {
			'tipo_cedula_empl': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('V-', 'V-'), ('E-', 'E-')],
				attrs = {
					'class': 'form-control',
				}
			),
			'cedula_empl': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Cedula'
				}
			),
			'nombre_empl': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Nombre'
				}
			),
			'apellido_empl': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Apellido'
				}
			),
			'tipo_telefono_empl': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('0412-', '0412-'), ('0414-', '0414-'), ('0416-', '0416-'), ('0424-', '0424-'), ('0426-', '0426-')],
				attrs = {
					'class': 'form-control'
				}
			),
			'telefono_empl': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Telefono de movil'
				}
			),
			'direccion_exacta': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Dirección',
					'rows': '1'
				}
			),
			'cargo': forms.Select(
				choices=[('','SELECCIONA UNA OPCIÓN'), ('ADMINISTRADOR', 'ADMINISTRADOR'), ('ALMACENISTA', 'ALMACENISTA'), ('ATENCIÓN AL CLIENTE', 'ATENCIÓN AL CLIENTE')],
				attrs = {
					'class': 'form-control'
				}
			)
		}


class FacturaForm(forms.ModelForm):
	class Meta:
		model = Factura
		fields = ('cod_pac', 'cod_empl', 'descripcion', 'id_producto', 'cantidad',)
		label = {
			'cod_pac': 'Paciente',
			'cod_empl': 'Empleado',
			'descripcion': 'Descripcion de la Factura',
			'id_producto': 'Producto',
			'cantidad': 'Cantidad',
		}
		widgets = {
			'cod_pac': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'cod_empl': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'descripcion': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Descripción de la Factura',
					'rows': '1'
				}
			),
			'id_producto': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'cantidad': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad del Producto'
				}
			),
		}


class Tipo_movForm(forms.ModelForm):
	class Meta:
		model = Tipo_mov
		fields = ('descripcion',)
		label = {
			'descripcion': 'Descripcion del Movimiento'
		}
		widgets = {
			'descripcion': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Descripción del Movimiento',
					'rows': '1'
				}
			),
		}


class Movimiento_inventarioForm(forms.ModelForm):
	class Meta:
		model = Movimiento_inventario
		fields = ('motivo_mov', 'tipo_mov', 'cod_empl', 'id_producto', 'cantidad',)
		label = {
			'motivo_mov': 'Motivo del Movimiento',
			'tipo_mov': 'Tipo de Movimiento',
			'cod_empl': 'Empleado',
			'id_producto': 'Producto',
			'cantidad': 'Cantidad',
		}
		widgets = {
			'motivo_mov': forms.Textarea(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Motivo del Movimiento',
					'rows': '1'
				}
			),
			'tipo_mov': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'cod_empl': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'id_producto': forms.Select(
				attrs = {
					'class':'form-control'
				}
			),
			'cantidad': forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder': 'Cantidad del Producto'
				}
			),
		}