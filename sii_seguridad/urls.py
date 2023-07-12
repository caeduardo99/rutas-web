from django.urls import path
from rutas_vendedor import views
from sii_seguridad.vistas.autenticacion_vista import login, signout

urlpatterns = [
    # URL para la página principal (home)
    path('home/', views.home, name='home'),
    # URL para la página del mapa de rutas
    path('rutas/', views.mapa),
    # URL para la página de inicio de sesión (login)
    path('', login),
    # URL para la página de cierre de sesión (logout)
    path('logout/', signout),
    # URL para la página de vendedores
    path('vendedor/', views.vendedor),
    
]
