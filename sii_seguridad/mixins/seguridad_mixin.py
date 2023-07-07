from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured


class PermisosRequeridos(PermissionRequiredMixin):
    modules_required = None

    def get_modules_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
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
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            return []
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):

        if isinstance(self.request.user, AnonymousUser):
            return False

        permissions = self.get_permission_required()
        modules = self.get_modules_required()

        return self.request.user.has_perms(permissions) and self.request.user.has_modules(modules) and True
