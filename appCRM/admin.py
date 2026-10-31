from django.contrib import admin

from .models import Cliente
from .forms import ClienteForms


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForms

    list_display = (
        'id',
        'name',
        'company',
        'email',
        'phone',
        'status',
        'created_at'
    )

    list_filter = ('status',)
    search_fields = ('name', 'company', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
