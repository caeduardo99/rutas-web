from sii_seguridad.configuracion import constantes_configuracion as const
from sii_seguridad.logica_negocio import cifrado_logica as cifrado
from sii_seguridad.models import Usuario


def autenticar(usuario, password):
    clave_encriptada = cifrado.cifrar_texto(password, const.CLAVE_LOGIN)
    return Usuario.objects.filter(id=usuario, clave=clave_encriptada).first()


def verifica_modulo(usuario):
    """
    Verifica el módulo del usuario y realiza alguna lógica adicional.

    :param usuario: Usuario para verificar el módulo.
    """
    # Realiza la lógica para verificar el módulo del usuario
    # Puedes acceder a las propiedades y métodos del objeto 'usuario' para obtener información adicional
    # ...

    pass
