from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

from sii_seguridad.formularios.autenticacion_form import LoginForm

def login(request):
    """
    Vista para el inicio de sesión.
    """
    message = None
    if request.user.is_authenticated:
        next = request.GET.get('next', '/home')
        return redirect(next)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            # limita la sesion segun la configuracion
            # request.session.set_expiry(TIME_SESSION_AVAILABLE)
            login_django(request, user)
            datos_session = user.obtener_campos_session
            request.session['grupo_id'] = datos_session.get('grupo_id').CodGrupo
            request.session['usuario_id'] = datos_session.get('usuario_id')
            request.session['usuario_nombre'] = datos_session.get('usuario_nombre')

            return redirect('/home')
        else:
            message = "Usuario o clave incorrectos!"

    form = LoginForm()

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'autenticacion/signin.html', context)


@login_required
def signout(request):
    """
    Vista para el cierre de sesión.
    """
    logout_django(request)
    return redirect('/')
