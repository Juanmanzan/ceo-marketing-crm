from django.urls import path
from .views.dashboard import resumenClientes
from .views.clientes import (
    listarClientes, 
    verCliente, 
    crearCliente, 
    actualizarCliente, 
    eliminarCliente
)
    

urlpatterns = [
    path('clientes/',listarClientes, name='listar_clientes'),
    path('clientes/crear/', crearCliente, name='crear_cliente'),
    path('clientes/resumen/', resumenClientes, name='resumen_clientes'),

    path('clientes/<int:id>/',verCliente, name='detalle_cliente'),
    path('clientes/<int:id>/actualizar/', actualizarCliente, name='actualizar_cliente'),
    path('clientes/<int:id>/eliminar/', eliminarCliente, name='eliminar_cliente'),
]
