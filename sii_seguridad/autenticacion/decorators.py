from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def permissions_required(perm=None, module=None, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):

        django_permissions = False
        sii_modules = False

        if isinstance(user, AnonymousUser):
            return False

        if not perm and not module:
            return True

        # Permissions Django
        if not perm:
            django_permissions = True
        else:
            if isinstance(perm, str):
                perms = (perm,)
            else:
                perms = perm
            # First check if the user has the permission (even anon users)
            if user.has_perms(perms):
                django_permissions = True

        # Sii Modules

        if isinstance(module, str):
            modules = (module,)
        else:
            modules = module

        if user.has_modules(modules):
            sii_modules = True

        # In case the 403 handler should be called raise the exception
        if raise_exception and (not django_permissions or not sii_modules):
            raise PermissionDenied
        # As the last resort, show the login form
        return django_permissions and sii_modules

    return user_passes_test(check_perms, login_url=login_url)
