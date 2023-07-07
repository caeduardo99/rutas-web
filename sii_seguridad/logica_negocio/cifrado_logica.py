# -*- coding: utf-8 -*-

from sii_seguridad.configuracion import constantes_configuracion as const
from sii_seguridad.exceptions.seguridad_exceptions import ClaveNoValidaException, ClaveDemasiadoCortaException


def cifrar_texto(valor, clave):
    return cifrar_descifrar_texto(valor, clave, 1)


def descifrar_texto(valor, clave):
    return cifrar_descifrar_texto(valor, clave, -1)


def cifrar_descifrar_texto(valor, clave, signo):
    resultado = ''

    # En esta parte se pierde mucha de la logica de encripcion
    valor_lower = valor.lower()

    if len(clave) < const.LONGITUD_CLAVE:
        raise ClaveDemasiadoCortaException

    if not validar_clave(clave):
        raise ClaveNoValidaException

    clave_desplazada = desplazar_cadena(clave, sumar_ASCII(clave))

    for i in range(0, len(valor_lower)):
        posicion_calculada = (i + 1) % len(clave_desplazada)
        caracter_actual = clave_desplazada[posicion_calculada:posicion_calculada + 1]

        valor_1 = ord(caracter_actual) % 10
        valor_2 = ord(valor_lower[i:i + 1]) + valor_1 * signo

        if valor_2 > const.LIMITE_MAYOR:
            valor_2 -= (const.LIMITE_MAYOR - const.LIMITE_MENOR)
        elif valor_2 < const.LIMITE_MENOR:
            valor_2 += (const.LIMITE_MAYOR - const.LIMITE_MENOR)
        resultado += chr(valor_2)

    return resultado


def validar_clave(clave):
    """
        Verifica si no repite un caracter en primeros LONGITUD_CLAVE caracteres

    :param clave: Clave que se va a validar
    :return: True si no se repite un caracter en los primeros LONGITUD_CLAVE caracteres
            False en caso contrario
    """
    for i in range(0, const.LONGITUD_CLAVE - 2):
        for j in range(i + 1, const.LONGITUD_CLAVE - 1):
            if clave[i:i + 1] == clave[j:j + 1]:
                return False
    return True


def desplazar_cadena(clave, valor_dividendo):
    residuo = valor_dividendo % len(clave)
    return f'{clave[residuo:len(clave)]}{clave[0:residuo]}'


def sumar_ASCII(clave):
    n = 0
    for i in range(0, len(clave)):
        n += ord(clave[i:i + 1])
    return n

# from sii_seguridad.utilidades.cifrado_utilidad import *
