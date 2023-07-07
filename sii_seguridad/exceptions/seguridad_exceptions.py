from sii_seguridad.configuracion.constantes_configuracion import LONGITUD_CLAVE


class ClaveNoValidaException(Exception):
    default_message = 'Clave de codificación no valida.'

    def __init__(self, message=None):
        if not message:
            message = self.default_message

        super().__init__(message)


class ClaveDemasiadoCortaException(Exception):
    default_message = f'Clave de debe contener más de {LONGITUD_CLAVE} caracteres'

    def __init__(self, message=None):
        if not message:
            message = self.default_message
        super().__init__(message)
