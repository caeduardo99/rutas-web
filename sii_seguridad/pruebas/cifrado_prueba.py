# -*- coding: utf-8 -*-

from unittest import TestCase

from sii_seguridad.exceptions import seguridad_exceptions as exc
from sii_seguridad.logica_negocio import cifrado_logica as cifrado


class CifradoTestCase(TestCase):
    """
    Pruebas Unitarias sobre el cifrado-descifrado de sii4

    """

    def setUp(self):
        """
            Inicializacion de variables para el cifrado-descifrado
        """
        self.clave_pequenia = '1234'
        self.clave_invalida = 'si4i123'
        self.clave_login = 'Usuario'
        self.usuario_vacio = ''
        self.cifrar = 1
        self.descifrar = -1
        self.valores_validos = {
            # '@Qyfw/(9': 'Gu~g|4/@',
            'marco': 'tewdt',
            'myuquilima': 't}zrznspqf',
            '26982': '9:>97',
            '': '',
        }
        self.valores_invalidos = {
            'Marco': 'as',
            '26982': 'fr',
            '@Qyfw/(9': 'hy',
            '': '1123'
        }

    def test_clave_pequenia_causa_excepcion(self):
        """

        :return:
        """
        self.assertRaises(
            exc.ClaveDemasiadoCortaException,
            cifrado.cifrar_descifrar_texto,
            self.usuario_vacio,
            self.clave_pequenia,
            self.cifrar
        )

    def test_clave_erronea_causa_excepcion(self):
        """

        :return:
        """
        self.assertRaises(
            exc.ClaveNoValidaException,
            cifrado.cifrar_descifrar_texto,
            self.usuario_vacio,
            self.clave_invalida,
            self.cifrar
        )

    def test_cifrado_correcto(self):
        """

        :return:
        """
        for clave, valor in self.valores_validos.items():
            encriptado = cifrado.cifrar_texto(clave, self.clave_login)
            self.assertEqual(valor, encriptado)

    def test_cifrado_incorrecto(self):
        """

        :return:
        """
        for clave, valor in self.valores_invalidos.items():
            encriptado = cifrado.cifrar_texto(clave, self.clave_login)
            self.assertNotEqual(valor, encriptado)


    def test_descifrado_correcto(self):
        """

        :return:
        """
        for clave, valor in self.valores_validos.items():
            encriptado = cifrado.descifrar_texto(valor, self.clave_login)
            self.assertEqual(clave, encriptado)

    def test_descifrado_incorrecto(self):
        """

        :return:
        """
        for clave, valor in self.valores_invalidos.items():
            encriptado = cifrado.descifrar_texto(valor, self.clave_login)
            self.assertNotEqual(clave, encriptado)
