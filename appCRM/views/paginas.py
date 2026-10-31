from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def mostrarDashboard(request):
    return render(request, "pages/dashboard.html")