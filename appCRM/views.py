from django.shortcuts import render
from django.http import JsonResponse
from .models import Cliente
from django.views.decorators.http import require_GET
from django.http import HttpResponse


@require_GET
def listarClientes(request):

    cursor = request.GET.get('cursor')

    limite = 10

    ## consultamos todos los usaurios y los ordenamos 
    clientesQuery = Cliente.objects.all().order_by('id')

    if cursor:
        try:
            if (cursor < 0):
                    error = {
                        "error": "El valor ingresado no es válido",
                        "status": 400
                    }
                    return JsonResponse(error)
            
            clientesQuery = clientesQuery.filter(id__gt=int(cursor))
            
        except ValueError:
           
           error = {
                "error": "El valor ingresado no es válido",
                "status": 400
            }
           return JsonResponse(error)


    clientesQuery = clientesQuery.values(
        'id', 
        'name', 
        'company', 
        'email', 
        'phone', 
        'status',
        'created_at'
    )

    clientesQuery = clientesQuery[:limite + 1]

    clientesLista = list(clientesQuery)
    
    existeOtraPagina = len(clientesLista) > limite
    cursor_next = None

    if(existeOtraPagina):
        clientesLista.pop()
        cursor_next = clientesLista[-1]['id']

    ## armar respuesta http

    data = {
        "clientes": clientesLista,
        "totalClientes": Cliente.objects.count(),
        "paginacion": {
            "existeOtraPagina": existeOtraPagina,
            "cursor_next": cursor_next
        }
    }

    return JsonResponse(data)

