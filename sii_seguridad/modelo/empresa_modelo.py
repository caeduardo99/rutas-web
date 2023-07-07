from django.db import models


class Empresa(models.Model):
    id = models.CharField(max_length=10, db_column='CODEMPRESA', primary_key=True)
    descripcion = models.CharField(max_length=50)
    tipo_base_datos = models.IntegerField(db_column='TIPODB')
    nombre_base_datos = models.CharField(max_length=20, db_column='NOMBREDB')
    server = models.CharField(max_length=30)
    usuario = models.CharField(max_length=20, db_column='USERNAME')
    password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'EMPRESA'
