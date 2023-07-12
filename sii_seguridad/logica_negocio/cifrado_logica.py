# -*- coding: utf-8 -*-

from sii_seguridad.configuracion import constantes_configuracion as const
from sii_seguridad.exceptions.seguridad_exceptions import ClaveNoValidaException, ClaveDemasiadoCortaException


def cifrar_texto(valor, clave):
    """
    Cifra un texto utilizando una clave dada.

    :param valor: Texto a cifrar.
    :param clave: Clave de cifrado.
    :return: Texto cifrado.
    """
    return cifrar_descifrar_texto(valor, clave, 1)


def descifrar_texto(valor, clave):
    """
    Descifra un texto cifrado utilizando una clave dada.

    :param valor: Texto cifrado.
    :param clave: Clave de cifrado.
    :return: Texto descifrado.
    """
    return cifrar_descifrar_texto(valor, clave, -1)


def cifrar_descifrar_texto(valor, clave, signo):
    """
    Cifra o descifra un texto utilizando una clave y un signo dado.

    :param valor: Texto a cifrar o descifrar.
    :param clave: Clave de cifrado.
    :param signo: Signo (-1 para descifrar, 1 para cifrar).
    :return: Texto cifrado o descifrado.
    """
    resultado = ''

    # En esta parte se pierde mucha de la lógica de encripción
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
    Verifica si no se repite un caracter en los primeros LONGITUD_CLAVE caracteres de la clave.

    :param clave: Clave que se va a validar.
    :return: True si no se repite un caracter en los primeros LONGITUD_CLAVE caracteres, False en caso contrario.
    """
    for i in range(0, const.LONGITUD_CLAVE - 2):
        for j in range(i + 1, const.LONGITUD_CLAVE - 1):
            if clave[i:i + 1] == clave[j:j + 1]:
                return False
    return True


def desplazar_cadena(clave, valor_dividendo):
    """
    Desplaza los caracteres de la cadena clave según el valor del dividendo.

    :param clave: Clave que se va a desplazar.
    :param valor_dividendo: Valor del dividendo utilizado para el desplazamiento.
    :return: Cadena clave desplazada.
    """
    residuo = valor_dividendo % len(clave)
    return f'{clave[residuo:len(clave)]}{clave[0:residuo]}'


def sumar_ASCII(clave):
    """
    Suma los valores ASCII de los caracteres de la clave.

    :param clave: Clave para la cual se sumarán los valores ASCII.
    :return: Suma de los valores ASCII de los caracteres de la clave.
    """
    n = 0
    for i in range(0, len(clave)):
        n += ord(clave[i:i + 1])
    return n
