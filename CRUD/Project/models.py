from django.db import models
import time
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
#------------------------------ Usuario ------------------------------#

class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombre, apellido, cargo, paciente, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username = username,
            nombre = nombre,
            apellido = apellido,
            email = self.normalize_email(email),
            cargo = cargo,
            paciente = paciente
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username, nombre, apellido, email, cargo, password, paciente):
        usuario = self.create_user(
            email,
            username = username,
            nombre = nombre,
            apellido = apellido,
            password = password,
            cargo = cargo,
            paciente = paciente
        )
        usuario.cargo = 'ADMINISTRADOR'
        usuario.save()
        return usuario


#------------------------------ Zona ------------------------------#


class Zona(models.Model):
    id_zona = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    zona_residencia = models.CharField(
        max_length=60, blank=False, null=False)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        ordering = ['zona_residencia']

    def __str__(self):
        return f'{self.zona_residencia}'

    def save(self, *args, **kwargs):
        self.zona_residencia = (self.zona_residencia).upper()
        return super(Zona, self).save(*args, **kwargs)


#------------------------------ Representante ------------------------------#


class Representante(models.Model):
    cod_repr = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    tipo_cedula_repr = models.CharField(
        max_length=2, blank=False, null=False)
    cedula_repr = models.CharField(
        'Cedula', unique=True, max_length=8, validators=[MinLengthValidator(7)], blank=False, null=False)
    nombre_repr = models.CharField(
        'Nombre', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    apellido_repr = models.CharField(
        'Apellido', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    parentesco = models.CharField(
        max_length=20, blank=False, null=False)

    class Meta:
        verbose_name = 'Representante'
        verbose_name_plural = 'Representantes'
        ordering = ['cedula_repr']

    def __str__(self):
        return f'{self.cedula_repr}'

    def save(self, *args, **kwargs):
        self.nombre_repr = (self.nombre_repr).upper()
        self.apellido_repr = (self.apellido_repr).upper()
        return super(Representante, self).save(*args, **kwargs)


#------------------------------ Paciente ------------------------------#


class Paciente(models.Model):
    cod_pac = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    tipo_cedula_pac = models.CharField(
        max_length=2, blank=False, null=False)
    cedula_pac = models.CharField(
        'Cedula', unique=True, max_length=8, validators=[MinLengthValidator(7)], blank=False, null=False)
    nombre_pac = models.CharField(
        'Nombre', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    apellido_pac = models.CharField(
        'Apellido', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    tipo_telefono_pac = models.CharField(
        max_length=5, blank=False, null=False)
    telefono_pac = models.CharField(
        'Telefono', max_length=7, validators=[MinLengthValidator(7)], blank=False, null=False)
    email_pac = models.EmailField(
        'Correo electrónico', unique=True, max_length=100, blank=False, null=False)
    cargo_pac = models.CharField(
        'Cargo', max_length=30, validators=[MinLengthValidator(2)], blank=False, null=False)
    id_zona = models.ForeignKey(
        Zona, verbose_name='Zona', on_delete=models.PROTECT, blank=False, null=False)
    sexo_pac = models.CharField(
        'Sexo',max_length=10, blank=False, null=False)
    fecha_nacimiento_pac = models.DateField(
        'Fecha de nacimiento', auto_now=False, blank=False, null=False)
    embarazada = models.CharField(
        'Embarazada',max_length=2, blank=True, null=True)
    cod_repr = models.ForeignKey(
        Representante, verbose_name='Representante', on_delete=models.PROTECT, blank=True, null=True)
    constancia_residencia = models.FileField(
        'Constancia de Residencia', upload_to='constancias_residencia/', storage=None, max_length=200, blank=False, null=False)
    username_pac = models.CharField(
        'Nombre de usuario', unique=True, max_length=100)
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['cedula_pac']

    def __str__(self):
        return f'{self.nombre_pac} {self.apellido_pac}'

    def save(self, *args, **kwargs):
        self.nombre_pac = (self.nombre_pac).upper()
        self.apellido_pac = (self.apellido_pac).upper()
        return super(Paciente, self).save(*args, **kwargs)

@receiver(post_save, sender=Paciente)
def crear_usuario_paciente(sender, instance, created, **kwargs):
    if created:
        # Creamos el usuario solo si el paciente es nuevo
        if not Usuario.objects.filter(username=instance.username_pac).exists():
            Usuario.objects.create(
                username=instance.username_pac,
                nombre=instance.nombre_pac,
                apellido=instance.apellido_pac,
                email=instance.email_pac,
                cargo=instance.cargo_pac,
                paciente=instance.cod_pac,
                password=instance.password
            )


#------------------------------ Ubicación ------------------------------#


class Ubicacion(models.Model):
    id_zona = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    ubicacion = models.CharField(
        'Ubicación', max_length=60, blank=False, null=False)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['ubicacion']

    def __str__(self):
        return f'{self.ubicacion}'

    def save(self, *args, **kwargs):
        self.ubicacion = (self.ubicacion).upper()
        return super(Ubicacion, self).save(*args, **kwargs)


#------------------------------ Tipo de Insumo ------------------------------#


class Tipo_insumo(models.Model):
    id_tipo_insumo = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    nombre_tipo_insumo = models.CharField(
        'Tipo del Insumo', max_length=60, blank=False, null=False)

    class Meta:
        verbose_name = 'Tipo de insumo'
        verbose_name_plural = 'Tipo de insumos'
        ordering = ['nombre_tipo_insumo']

    def __str__(self):
        return f'{self.nombre_tipo_insumo}'

    def save(self, *args, **kwargs):
        self.nombre_tipo_insumo = (self.nombre_tipo_insumo).upper()
        return super(Tipo_insumo, self).save(*args, **kwargs)


#------------------------------ Lote ------------------------------#


class Lote(models.Model):
    id_lote = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    lote = models.CharField(
        'Lote', max_length=60, blank=False, null=False)
    canti_pro = models.CharField(
        'Cantidad del Producto', max_length=4, blank=False, null=False)
    fecha_lote = models.DateField(
        'Fecha del Lote', auto_now=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        ordering = ['lote']

    def __str__(self):
        return f'{self.lote}'

    def save(self, *args, **kwargs):
        self.lote = (self.lote).upper()
        return super(Lote, self).save(*args, **kwargs)


#------------------------------ Laboratorio ------------------------------#


class Laboratorio(models.Model):
    id_laboratorio = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    nombre_laboratorio = models.CharField(
        max_length=60, blank=False, null=False)

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        ordering = ['nombre_laboratorio']

    def __str__(self):
        return f'{self.nombre_laboratorio}'

    def save(self, *args, **kwargs):
        self.nombre_laboratorio = (self.nombre_laboratorio).upper()
        return super(Laboratorio, self).save(*args, **kwargs)


#------------------------------ Producto ------------------------------#


class Producto(models.Model):
    id_producto = models.AutoField(
        'Codigo del Producto', primary_key=True, blank=False, null=False)
    nombre_producto = models.CharField(
        'Nombre del Producto', max_length=40, validators=[MinLengthValidator(2)], blank=False, null=False)
    id_ubicacion = models.ForeignKey(
        Ubicacion, verbose_name='Ubicación', on_delete=models.PROTECT, blank=False, null=False)
    id_tipo_insumo = models.ForeignKey(
        Tipo_insumo, verbose_name='Tipo de insumo', on_delete=models.PROTECT, blank=False, null=False)
    id_lote = models.ForeignKey(
        Lote, verbose_name='Lote', on_delete=models.PROTECT, blank=False, null=False)
    id_laboratorio = models.ForeignKey(
        Laboratorio, verbose_name='Laboratorio', on_delete=models.PROTECT, blank=False, null=False)
    limite = models.CharField(
        'Limite por parciente',max_length=3, blank=False, null=False)
    stock_max = models.CharField(
        'Stock maxino', max_length=5, blank=False, null=False)
    stock_min = models.CharField(
        'Stock minimo', max_length=5, blank=False, null=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre_producto']

    def __str__(self):
        return f'{self.nombre_producto}'

    def save(self, *args, **kwargs):
        self.nombre_producto = (self.nombre_producto).upper()
        return super(Producto, self).save(*args, **kwargs)


#------------------------------ Solicitud de Medicamento ------------------------------#


class Solicitud(models.Model):
    id_soli = models.AutoField(
        'Codigo del Producto', primary_key=True, blank=False, null=False)
    fecha_soli = models.DateField(
        'Fecha de la Solicitud', auto_now=True, blank=False, null=False)
    cod_pac = models.ForeignKey(
        Paciente, verbose_name='Paciente', on_delete=models.PROTECT, blank=False, null=False)
    descripcion_soli = models.TextField(
        'Descripción de la Solicitud', blank=False, null=False)
    id_producto = models.ManyToManyField(
        Producto, verbose_name='Producto')
    cantidad = models.CharField(
        'Cantidad del Producto',max_length=3, blank=False, null=False)
    recipe = models.FileField(
        'Recipe', upload_to='recipes/', storage=None, max_length=200, blank=False, null=False)
    
    class Meta:
        verbose_name = 'Solicitud de Medicamento'
        verbose_name_plural = 'Solicitud de Medicamentos'
        ordering = ['fecha_soli']

    def __str__(self):
        return f'{self.descripcion_soli}'

    def save(self, *args, **kwargs):
        self.descripcion_soli = (self.descripcion_soli).upper()
        return super(Solicitud, self).save(*args, **kwargs)


#------------------------------ Empleado ------------------------------#


class Empleado(models.Model):
    cod_empl = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    tipo_cedula_empl = models.CharField(
        max_length=2, blank=False, null=False)
    cedula_empl = models.CharField(
        'Cedula', unique=True, max_length=8, validators=[MinLengthValidator(7)], blank=False, null=False)
    nombre_empl = models.CharField(
        'Nombre', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    apellido_empl = models.CharField(
        'Apellido', max_length=15, validators=[MinLengthValidator(2)], blank=False, null=False)
    tipo_telefono_empl = models.CharField(
        max_length=5, blank=False, null=False)
    telefono_empl = models.CharField(
        'Telefono', max_length=7, validators=[MinLengthValidator(7)], blank=False, null=False)
    direccion_exacta = models.TextField(
        'Dirección', blank=False, null=False)
    cargo = models.CharField(
        'Cargo', max_length=30, validators=[MinLengthValidator(2)], blank=False, null=False)
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['cedula_empl']

    def __str__(self):
        return f'{self.nombre_empl} {self.apellido_empl}'

    def save(self, *args, **kwargs):
        self.nombre_empl = (self.nombre_empl).upper()
        self.apellido_empl = (self.apellido_empl).upper()
        return super(Empleado, self).save(*args, **kwargs)

        
#------------------------------ Factura ------------------------------#


class Factura(models.Model):
    cod_fac = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    fecha_fac = models.DateField(
        'Fecha de la Factura', auto_now=True, blank=False, null=False)
    cod_pac = models.ForeignKey(
        Paciente, verbose_name='Paciente', on_delete=models.PROTECT, blank=False, null=False)
    cod_empl = models.ForeignKey(
        Empleado, verbose_name='Empleado', on_delete=models.PROTECT, blank=False, null=False)
    descripcion = models.TextField(
        'Descripción de la Factura', blank=False, null=False)
    id_producto = models.ForeignKey(
        Producto, verbose_name='Producto', on_delete=models.PROTECT, blank=False, null=False)
    cantidad = models.CharField(
        'Cantidad del Producto', max_length=3, blank=False, null=False)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['fecha_fac']

    def __str__(self):
        return f'{self.fecha_fac} {self.cod_pac}'

    def save(self, *args, **kwargs):
        self.descripcion = (self.descripcion).upper()
        return super(Factura, self).save(*args, **kwargs)


#------------------------------ Tipo de Movimiento ------------------------------#


class Tipo_mov(models.Model):
    tipo_mov = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    descripcion = models.TextField(
        'Descripción del Movimiento', blank=False, null=False)

    class Meta:
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimientos'
        ordering = ['descripcion']

    def __str__(self):
        return f'{self.descripcion}'

    def save(self, *args, **kwargs):
        self.descripcion = (self.descripcion).upper()
        return super(Tipo_mov, self).save(*args, **kwargs)


#------------------------------ Movimiento de Inventario ------------------------------#


class Movimiento_inventario(models.Model):
    id_mov = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    fecha_mov = models.DateField(
        'Fecha del Movimiento', auto_now=True, blank=False, null=False)
    motivo_mov = models.TextField(
        'Motivo del Movimiento', blank=False, null=False)
    tipo_mov = models.ForeignKey(
        Tipo_mov, verbose_name='Tipo de Movimiento', on_delete=models.PROTECT, blank=False, null=False)
    cod_empl = models.ForeignKey(
        Empleado, verbose_name='Empleado', on_delete=models.PROTECT, blank=False, null=False)
    id_producto = models.ForeignKey(
        Producto, verbose_name='Producto', on_delete=models.PROTECT, blank=False, null=False)
    cantidad = models.CharField(
        'cantidad del Producto', max_length=3, blank=False, null=False)

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['fecha_mov']

    def __str__(self):
        return f'{self.fecha_mov} {self.tipo_mov}'

    def save(self, *args, **kwargs):
        self.motivo_mov = (self.motivo_mov).upper()
        return super(Movimiento_inventario, self).save(*args, **kwargs)


#------------------------------ Usuario ------------------------------#

class Usuario(AbstractBaseUser):
    cod_usuario = models.AutoField(
        'Codigo', primary_key=True, blank=False, null=False)
    username = models.CharField(
        'Nombre de usuario', unique=True, max_length=100)
    nombre = models.CharField(
        'Nombre', max_length=16, validators=[MinLengthValidator(2)], blank=False, null=False)
    apellido = models.CharField(
        'Apellido', max_length=16, validators=[MinLengthValidator(2)], blank=False, null=False)
    email = models.EmailField(
        'Correo electrónico', unique=True, max_length=100, blank=False, null=False)
    cargo = models.CharField(
        'Cargo', max_length=30, validators=[MinLengthValidator(2)], blank=False, null=False)
    imagen = models.ImageField(
        'Foto de perfil', upload_to='perfil/', max_length=100, blank=True, null=True)
    objects = UsuarioManager()
    intentos_fallidos = models.PositiveIntegerField(default=0)
    cuenta_bloqueada = models.BooleanField(default=False)
    paciente = models.OneToOneField(Paciente, on_delete=models.SET_NULL, null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.username = (self.username).upper()
        self.nombre = (self.nombre).upper()
        self.apellido = (self.apellido).upper()
        self.email = (self.email).upper()
        return super(Usuario, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.cargo