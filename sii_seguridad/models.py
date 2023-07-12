from django.db import models
from sii_seguridad.modelo import permiso_modelo
from sii_seguridad.modelo.usuario_modelo import GrupoUsuario

class Usuario(models.Model):
    id = models.CharField(max_length=20, primary_key=True, db_column='CODUSUARIO')
    grupo = models.ForeignKey(GrupoUsuario, related_name='usuarios', on_delete=models.PROTECT, db_column='CODGRUPO')
    nombre = models.CharField(max_length=100, db_column='NOMBREUSUARIO')
    clave = models.CharField(max_length=100)
    es_supervisor = models.BooleanField(db_column='BANDSUPERVISOR')
    is_active = models.BooleanField(db_column='BANDVALIDA')
    modulos = models.CharField(max_length=200)
    last_login = models.DateTimeField(db_column='FECHAGRABADO')
    BandSupervisor = models.CharField(max_length=10, null=False, blank=False)
    BandValida = models.BooleanField(null=True, default=True)

    REQUIRED_FIELDS = ['grupo', ]
    USERNAME_FIELD = 'id'

    @property
    def obtener_campos_session(self):
        """
        Propiedad para obtener los campos de la sesión del usuario.
        """
        datos_session = {
            'grupo_id': self.grupo,
            'usuario_nombre': self.nombre,
            'usuario_id': self.id
        }
        return datos_session

    @property
    def is_anonymous(self):
        """
        Propiedad que indica si el usuario es anónimo.
        """
        return True

    @property
    def is_authenticated(self):
        """
        Propiedad que indica si el usuario está autenticado.
        Siempre devuelve True. Se utiliza en las plantillas para saber si el usuario ha sido autenticado.
        """
        return True

    @property
    def obtener_modulos(self):
        """
        Propiedad para obtener los módulos a los que tiene acceso el usuario.
        """
        return self.modulos.split(';')

    def has_perms(self, perms):
        """
        Verifica si el usuario tiene los permisos especificados.
        Si el usuario es supervisor o no está activo, se le otorgan todos los permisos.
        """
        if self.is_active and self.es_supervisor:
            return True

        if not self.is_active:
            return False

        for perm in perms:
            if self.grupo.permisos.filter(menus__parametro__contains=perm).count() == 0:
                return False

        return True

    def has_modules(self, modules):
        """
        Verifica si el usuario tiene acceso a los módulos especificados.
        Si el usuario es supervisor o no está activo, se le otorgan todos los módulos.
        """
        if self.is_active and self.es_supervisor:
            return True

        if not self.is_active:
            return False

        for module in modules:
            if module not in self.modulos:
                return False
        return True

    def __str__(self):
        """
        Representación en cadena del objeto Usuario.
        Devuelve el nombre del usuario.
        """
        return self.nombre

    class Meta:
        managed = False
        db_table = 'USUARIO'
