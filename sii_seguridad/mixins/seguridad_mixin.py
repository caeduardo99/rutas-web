from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured

class PermisosRequeridos(PermissionRequiredMixin):
    modules_required = None

    def get_modules_required(self):
        """
        Devuelve los módulos requeridos.
        Anula este método para anular el atributo modules_required.
        Debe devolver un iterable.
        """
        if self.modules_required is None:
            return []
        if isinstance(self.modules_required, str):
            perms = (self.modules_required,)
        else:
            perms = self.modules_required
        return perms

    def get_permission_required(self):
        """
        Devuelve los permisos requeridos.
        Anula este método para anular el atributo permission_required.
        Debe devolver un iterable.
        """
        if self.permission_required is None:
            return []
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        """
        Verifica si el usuario tiene los permisos y módulos requeridos.
        Devuelve True si el usuario tiene los permisos y módulos requeridos, False en caso contrario.
        """
        if isinstance(self.request.user, AnonymousUser):
            return False

        permissions = self.get_permission_required()
        modules = self.get_modules_required()

        return self.request.user.has_perms(permissions) and self.request.user.has_modules(modules) and True
