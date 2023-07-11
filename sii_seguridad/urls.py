from django.urls import path
from rutas_vendedor import views
from sii_seguridad.vistas.autenticacion_vista import login, signout

urlpatterns = [
    path('home/', views.home, name='home'),
    path('rutas/', views.mapa),
    path('', login),
    path('logout/', signout),
    path('vendedor/', views.vendedor),
]
