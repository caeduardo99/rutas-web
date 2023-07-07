import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.template import loader
import pandas as pd
from django.shortcuts import redirect
from datetime import datetime
from datetime import date


@login_required
def home(request):
    
    with connection.cursor() as cursor:
        query_visitas = '''
            SELECT
            FC.Nombre as Vendedor,
            PC.Nombre as Cliente, 
            CV.HoraVisita AS Cronograma,
            CV.Zona,
            V.FechaVisita,
            CASE
                WHEN V.IdVisita IS NOT NULL AND V.Visitado = 1 THEN 'Cumplida'
                ELSE 'No cumplida'
            END AS EstadoVisita,
            V.Latitud AS LatVisita,
            V.Longitud AS  LongVisita ,
            C.posGoogleMaps AS UbiCliente,
            CASE
                WHEN ABS(V.Latitud - CAST(SUBSTRING(C.posGoogleMaps, 1, CHARINDEX(',', C.posGoogleMaps) - 1) AS DECIMAL(18, 15))) <= 0.01
                    AND ABS(V.Longitud - CAST(SUBSTRING(C.posGoogleMaps, CHARINDEX(',', C.posGoogleMaps) + 1, LEN(C.posGoogleMaps)) AS DECIMAL(18, 15))) <= 0.01 THEN 'Aceptable'
                ELSE 'Posible discrepancia'
            END AS ValidacionVariacion
            FROM
            CronogramaVisitas CV
            LEFT JOIN Visitas V ON CV.IdVendedor = V.IdVendedor
                                AND CV.IdProvCli = V.IdProvCli
                                AND CV.Zona = V.Zona
                                AND CONVERT(DATE, CV.FechaVisita) = CONVERT(DATE, V.FechaVisita)
            LEFT JOIN PCProvCli C ON CV.IdProvCli = C.IdProvCli
            LEFT JOIN FCVendedor FC ON CV.IdVendedor = FC.IdVendedor
            LEFT JOIN PCProvCli PC ON CV.IdProvCli = PC.IdProvCli
            ORDER BY
            FC.Nombre,EstadoVisita;
            '''
        cursor.execute(query_visitas)
        resultados_visitas = cursor.fetchall()
        

        query_vendedores = '''
            SELECT *
            FROM FCVendedor;
        '''
        cursor.execute(query_vendedores)
        resultados_vendedores = cursor.fetchall()
        
        username = request.user
        print(request.user) 
        # Convertir los resultados en un DataFrame
        columns = [column[0] for column in cursor.description]

        # Crea el DataFrame con los resultados y las columnas
        df_vendedores = pd.DataFrame(resultados_vendedores, columns=columns)
        df_vendedores = df_vendedores.to_dict("records")
        

    # Renderizar la plantilla con los resultados
    template = loader.get_template('home.html')
    context = {
        'resultados_visitas': resultados_visitas,
        'df_vendedores': df_vendedores,
        'username': username
      
    }

    tabla_html = template.render(context)
    # Retornar la respuesta HTTP
    return HttpResponse(tabla_html)



@login_required
def mapa(request):
    fecha = request.GET.get('fecha')  # Obtener el valor del parámetro 'fecha' del request
    vendedor = request.GET.get('vendedor')  # Obtener el valor del parámetro 'vendedor' del request
    
    def obtener_vendedores():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM FCVendedor")
            vendedores = [row[2] for row in cursor.fetchall()]
        return vendedores

    if fecha or vendedor:
        with connection.cursor() as cursor:
            # Consulta para obtener las LatVisita y LonVisita por Vendedor en la fecha específica
            query = '''
                SELECT FC.Nombre as Vendedor, V.Latitud as LatVisita, V.Longitud as LonVisita, V.ingreso, V.FechaVisita, V.accion, V.observaciones, V.monto
                FROM Visitas V
                LEFT JOIN FCVendedor FC ON V.IdVendedor = FC.IdVendedor
                WHERE 1=1
            '''
            params = []

            if fecha:
                query += ' AND CONVERT(DATE, V.FechaVisita) = %s'
                params.append(fecha)

            if vendedor:
                query += ' AND FC.Nombre = %s'
                params.append(vendedor)

            query += ' AND (V.Latitud IS NOT NULL) ORDER BY FechaVisita'

            cursor.execute(query, params)
            resultados_visitas = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            # Crear el DataFrame con los resultados y las columnas
            df_mapa = pd.DataFrame(resultados_visitas, columns=columns)

            # Obtener las estadísticas de los vendedores
            estadisticas_vendedores = {}

            for vendedor in df_mapa['Vendedor'].unique():
                monto_pedido = df_mapa.loc[(df_mapa['Vendedor'] == vendedor) & (df_mapa['accion'] == 'Pedido'), 'monto'].sum()
                monto_cobro = df_mapa.loc[(df_mapa['Vendedor'] == vendedor) & (df_mapa['accion'] == 'Cobro'), 'monto'].sum()
                estadisticas_vendedores[vendedor] = {
                    'visitas': len(df_mapa[df_mapa['Vendedor'] == vendedor]),
                    'monto_pedido': monto_pedido,
                    'monto_cobro': monto_cobro
                }

            # Convertir el DataFrame a formato JSON
            df_mapa_json = df_mapa.to_json(orient='records')

    else:
        df_mapa_json = '[]'
        estadisticas_vendedores = {}

    template = loader.get_template('rutas.html')
    context = {
        'resultados_visitas': df_mapa_json,
        'vendedores': obtener_vendedores(),
        'selected_vendedor': vendedor,
        'estadisticas_vendedores': estadisticas_vendedores,
        'fecha' : fecha,
    }
    mapa_html = template.render(context)

    return HttpResponse(mapa_html)

