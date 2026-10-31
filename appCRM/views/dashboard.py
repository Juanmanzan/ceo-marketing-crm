from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from appCRM.models import Cliente, statusClient


@require_GET
def resumenClientes(request):
    # Calcular todos los indicadores en una sola consulta
    data = Cliente.objects.aggregate(
        totalClientes=Count('id'),
        prospectos=Count('id', filter=Q(status=statusClient.prospecto)),
        clientesActivos=Count('id', filter=Q(status=statusClient.cliente)),
        inactivos=Count('id', filter=Q(status=statusClient.inactivo))
    )

    return JsonResponse(data, status=200)
