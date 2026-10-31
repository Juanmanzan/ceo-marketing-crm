from django.urls import path
from .views import listarClientes

urlpatterns = [
    path('clientes/',listarClientes, name='listar_clientes')
]