from django.contrib import admin
from .models import Event, Ticket, Organizer  # Agregar Organizer

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'date', 'tickets_sold']  # Muestra el campo tickets_sold en la lista
    readonly_fields = ['tickets_sold']  # Hace que el campo sea solo de lectura en la interfaz de cambio

    # Definir el método personalizado para contar los tickets vendidos
    def tickets_sold(self, obj):
        return Ticket.objects.filter(event=obj).count()
    
    tickets_sold.short_description = 'Tickets Sold'  # Etiqueta para mostrar en la interfaz de administración

# Registrar los modelos en el admin
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket)
admin.site.register(Organizer)  # Registrar Organizer
