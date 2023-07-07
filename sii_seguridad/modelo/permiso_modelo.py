from django.db import models

from sii_seguridad.modelo.empresa_modelo import Empresa
from sii_seguridad.modelo.usuario_modelo import GrupoUsuario


class Permiso(models.Model):
    Id = models.IntegerField(unique=True, primary_key=True, db_column='Id', blank=False)
    grupo = models.ForeignKey(GrupoUsuario, related_name='permisos', db_column='CODGRUPO', on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, related_name='permisos', db_column='CODEMPRESA', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'PERMISO'


class PermisoMenu(models.Model):
    permiso = models.ForeignKey(Permiso, related_name='menus', db_column='IDPERMISO', on_delete=models.PROTECT)
    parametro = models.CharField(max_length=20, db_column='PARAM')

    class Meta:
        managed = False
        db_table = 'PERMISOMENU'


class PermisoTrans(models.Model):
    IdPermiso = models.IntegerField(primary_key=True, unique=True, db_column='IdPermiso', blank=False)
    CodTrans = models.CharField(max_length=10, null=False, blank=False)
    Crear = models.BooleanField(null=True, default=True)
    Ver = models.BooleanField(null=True, default=True)
    Modificar = models.BooleanField(null=True, default=True)
    Eliminar = models.BooleanField(null=True, default=True)
    Aprobar = models.BooleanField(null=True, default=True)
    Desaprobar = models.BooleanField(null=True, default=True)
    Despachar = models.BooleanField(null=True, default=True)
    Anular = models.BooleanField(null=True, default=True)

    class Meta:
        managed = False
        db_table = 'PermisoTrans'
        permissions = (
            ('PermisoTrans', 'Puede visualizar PermisoTrans'),
        )