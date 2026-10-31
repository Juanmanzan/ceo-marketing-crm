from django.shortcuts import render
from django.http import JsonResponse

def listarClientes(request):
    data = {
        
        'clientes': [],
        "total":0,
    }
    return JsonResponse(data)

# Create your views here.
