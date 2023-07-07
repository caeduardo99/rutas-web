from sii_seguridad.configuracion import constantes_configuracion as const
from sii_seguridad.logica_negocio import cifrado_logica as cifrado
from sii_seguridad.models import Usuario


def autenticar(usuario, password):
    clave_encriptada = cifrado.cifrar_texto(password, const.CLAVE_LOGIN)
    return Usuario.objects.filter(id=usuario, clave=clave_encriptada).first()


def verifica_modulo(usuario):
    a = usuario
    pass
