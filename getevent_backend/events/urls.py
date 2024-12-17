from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse
from . import views

urlpatterns = [
    # Eventos
    path('events/', views.event_list, name='event_list'),  # GET: Lista de eventos
    path('events/<int:id>/', views.event_detail, name='event_detail'),  # GET: Evento específico
    path('events/create/', views.event_create, name='event_create'),  # POST: Crear evento
    path('events/<int:id>/edit/', views.event_edit, name='event_edit'),  # PUT: Editar evento
    path('events/<int:id>/delete/', views.event_delete, name='event_delete'),  # DELETE: Eliminar evento
    path('events/<int:event_id>/register/', views.register_to_event, name='register_to_event'),  # POST: Registrar usuario en un evento

    # Tickets
    path('events/<int:event_id>/tickets/', views.ticket_list, name='ticket_list'),  # GET: Lista de tickets por evento
    path('events/<int:event_id>/tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),  # GET: Ticket específico
    path('events/<int:event_id>/tickets/create/', views.ticket_create, name='ticket_create'),  # POST: Crear ticket
    path('events/<int:event_id>/tickets/<int:ticket_id>/edit/', views.ticket_edit, name='ticket_edit'),  # PUT: Editar ticket
    path('events/<int:event_id>/tickets/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),  # DELETE: Eliminar ticket

    # Organizadores
    path('organizers/', views.organizer_list, name='organizer_list'),  # GET: Lista de organizadores
    path('organizers/<int:id>/', views.organizer_detail, name='organizer_detail'),  # GET: Organizador específico
    path('organizers/create/', views.organizer_create, name='organizer_create'),  # POST: Crear organizador
    path('organizers/<int:id>/edit/', views.organizer_edit, name='organizer_edit'),  # PUT: Editar organizador
    path('organizers/<int:id>/delete/', views.organizer_delete, name='organizer_delete'),  # DELETE: Eliminar organizador

    # Endpoints para Tokens JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtener token de acceso y refresco
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refrescar token

    # Ruta de prueba (opcional) para verificar si el servidor está funcionando
    path('health/', lambda request: JsonResponse({"status": "OK"}), name='health_check'),
]