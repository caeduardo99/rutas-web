from django.db import models


class GrupoUsuario(models.Model):
    CodGrupo = models.CharField(max_length=10, unique=True, primary_key=True, db_column='CodGrupo', blank=False)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GRUPO'
