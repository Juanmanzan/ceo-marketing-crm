from django.shortcuts import render
from django.http import JsonResponse
from appCRM.models import Cliente
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.db import IntegrityError
from ..forms import ClienteForms
from django.views.decorators.csrf import csrf_exempt
import json



@require_GET
def listarClientes(request):

    cursor = request.GET.get('cursor')

    limite = 10

    ## consultamos todos los usaurios y los ordenamos 
    clientesQuery = Cliente.objects.all().order_by('id')

    if cursor:
        try:
            if(int(cursor) < 0):
                  
                    return JsonResponse({
                        "error": "El valor ingresado no es válido"
                    }, status=404)
            
            clientesQuery = clientesQuery.filter(id__gt=int(cursor))
            
        except ValueError:
           
           return JsonResponse({
               "error": "El valor ingresado no es válido",
           }, status=400)


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

    return JsonResponse(data, status=200)


@require_GET
def verCliente(request, id):
    try:
        cliente = Cliente.objects.values(
            'id', 
            'name', 
            'company', 
            'email',
            'phone',
            'status'
        ).get(id=id)

        data = {
            "cliente": cliente
        }

        return JsonResponse(data, status=200)

    except Cliente.DoesNotExist:
        return JsonResponse({
                "error": "Cliente no encontrado"
            }, status=404
        )


@require_POST
def crearCliente(request):
    try:
        # obtener el cuerpo del mensaje de la peticion htttp
        cuerpo_peticion = request.body.decode('utf-8')
        cliente = json.loads(cuerpo_peticion)

        if not isinstance(cliente, dict):
            return JsonResponse({
                "error": "Se esperaba un objeto JSON con los datos del cliente"
            }, status=400)

        cliente.setdefault("status", "Prospecto")

        form = ClienteForms(cliente)

        if not form.is_valid():
            return JsonResponse({
                "errors": form.errors.get_json_data()
            }, status=400)


        cliente_nuevo = form.save()

        data ={
            "mensaje": "Cliente creado exitosamente",
            "cliente": {

                "id": cliente_nuevo.id,
                "name": cliente_nuevo.name,
                "company": cliente_nuevo.company,
                "email": cliente_nuevo.email,
                "phone": cliente_nuevo.phone,
                "status": cliente_nuevo.status,
                "created_at": cliente_nuevo.created_at 
            }
        }

        return JsonResponse(data, status=201)  
        
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "El formato JSON de la petición no es válido"
            }, status = 400)

    except IntegrityError:
        return JsonResponse({
            "error": "No se pudo registrar el cliente por un conflicto de datos"
        }, status=409)


@require_http_methods(["PUT"])
def actualizarCliente(request, id):

    try:

        cliente = Cliente.objects.get(id=id)

        cuerpo_peticion = request.body.decode('utf-8')
        campos_actualizar = json.loads(cuerpo_peticion)

        if not isinstance(campos_actualizar, dict):
            return JsonResponse({
                "error": "Se esperaba un objeto JSON con los datos del cliente"
            }, status=400)

        form = ClienteForms(campos_actualizar, instance=cliente)

        if not form.is_valid():
            return JsonResponse({
                "errors": form.errors.get_json_data()
            }, status=400)

        cliente_actualizado = form.save()

        data ={
                "mensaje": "Cliente actualizado exitosamente",
                "cliente": {
    
                    "id": cliente_actualizado.id,
                    "name": cliente_actualizado.name,
                    "company": cliente_actualizado.company,
                    "email": cliente_actualizado.email,
                    "phone": cliente_actualizado.phone,
                    "status": cliente_actualizado.status,
                    "updated_at": cliente_actualizado.updated_at
                }
            }

        return JsonResponse(data, status=200)  

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "El formato JSON de la petición no es válido"
            }, status = 400)

    except IntegrityError:
        return JsonResponse({
            "error": "No se pudo registrar el cliente por un conflicto de datos"
        }, status=409)

    except Cliente.DoesNotExist:
        return JsonResponse({
            "error": "Cliente no encontrado"
        }, status=404)

    
@require_http_methods(["DELETE"])
def eliminarCliente(request, id):

    try:

        cliente = Cliente.objects.get(id=id)

        nombre_cliente = cliente.name

        cliente.delete()

        return JsonResponse({
            "mensaje": "Cliente eliminado exitosamente",
            "id": id,
            "name": nombre_cliente
        }, status=200)


    except Cliente.DoesNotExist:
        return JsonResponse({
            "error": "Cliente no encontrado"
        }, status=404)
    