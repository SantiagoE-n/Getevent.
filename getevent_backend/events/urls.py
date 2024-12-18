from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse
from . import views

urlpatterns = [
    # Eventos
    path('events/', views.event_list, name='event_list'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:id>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:event_id>/register/', views.register_to_event, name='register_to_event'),

    # Tickets
    path('events/<int:event_id>/tickets/', views.ticket_list, name='ticket_list'),
    path('events/<int:event_id>/tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('events/<int:event_id>/tickets/create/', views.ticket_create, name='ticket_create'),

    # Organizadores
    path('organizers/', views.organizer_list, name='organizer_list'),
    path('organizers/<int:id>/', views.organizer_detail, name='organizer_detail'),
    path('organizers/<int:id>/edit/', views.organizer_edit, name='organizer_edit'),

    # Usuarios
    path('register/', views.user_register, name='user_register'),  # Endpoint de registro de usuarios
    path('profile/', views.user_profile, name='user_profile'),     # Endpoint para obtener el perfil del usuario autenticado

    # JWT Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Health Check (opcional)
    path('health/', lambda request: JsonResponse({"status": "OK"}), name='health_check'),
]