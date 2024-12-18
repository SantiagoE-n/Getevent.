from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Event, Ticket, Organizer, User
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password  # Para cifrar contraseñas
import json

# Eventos
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_list(request):
    events = Event.objects.all()
    event_data = []
    for event in events:
        tickets_sold = Ticket.objects.filter(event=event).count()
        event_data.append({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'location': event.location,
            'date': event.date,
            'is_private': event.is_private,
            'tickets_sold': tickets_sold
        })
    return JsonResponse({'events': event_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_detail(request, id):
    try:
        event = Event.objects.get(pk=id)
        tickets = Ticket.objects.filter(event=event).values('id', 'user__username', 'price', 'purchase_date')
        return JsonResponse({
            'event': model_to_dict(event),
            'tickets': list(tickets)
        })
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_create(request):
    try:
        data = json.loads(request.body)
        event = Event.objects.create(
            name=data['name'],
            date=data['date'],
            location=data['location'],
            description=data.get('description', ''),
            is_private=data.get('is_private', False),
            password=data.get('password', None)
        )
        return JsonResponse({'event': model_to_dict(event)}, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_to_event(request, id):
    try:
        event = Event.objects.get(pk=id)
        user = request.user
        ticket, created = Ticket.objects.get_or_create(event=event, user=user)
        if not created:
            return JsonResponse({'message': 'You are already registered for this event.'}, status=400)
        return JsonResponse({'message': f'Registered successfully to {event.name}'}, status=201)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def event_edit(request, id):
    try:
        event = Event.objects.get(pk=id)
        data = json.loads(request.body)
        event.name = data.get('name', event.name)
        event.date = data.get('date', event.date)
        event.location = data.get('location', event.location)
        event.description = data.get('description', event.description)
        event.is_private = data.get('is_private', event.is_private)
        event.password = data.get('password', event.password)
        event.save()
        return JsonResponse({'event': model_to_dict(event)})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def event_delete(request, id):
    try:
        event = Event.objects.get(pk=id)
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'}, status=204)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

# Tickets
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_list(request, event_id):
    tickets = Ticket.objects.filter(event_id=event_id)
    ticket_data = [{'id': ticket.id, 'user': ticket.user.username, 'price': ticket.price} for ticket in tickets]
    return JsonResponse({'tickets': ticket_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ticket_detail(request, event_id, ticket_id):
    try:
        ticket = Ticket.objects.get(event_id=event_id, pk=ticket_id)
        return JsonResponse({'ticket': model_to_dict(ticket)})
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ticket_create(request, event_id):
    try:
        data = json.loads(request.body)
        ticket = Ticket.objects.create(
            event_id=event_id,
            user_id=data['user'],
            price=data['price']
        )
        return JsonResponse({'ticket': model_to_dict(ticket)}, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

# Organizadores
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organizer_list(request):
    organizers = Organizer.objects.all()
    organizer_data = [{'id': organizer.id, 'name': organizer.name, 'contact_info': organizer.contact_info} for organizer in organizers]
    return JsonResponse({'organizers': organizer_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organizer_detail(request, id):
    try:
        organizer = Organizer.objects.get(pk=id)
        return JsonResponse({'organizer': model_to_dict(organizer)})
    except Organizer.DoesNotExist:
        return JsonResponse({'error': 'Organizer not found'}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def organizer_edit(request, id):
    try:
        organizer = Organizer.objects.get(pk=id)
        data = json.loads(request.body)
        organizer.name = data.get('name', organizer.name)
        organizer.contact_info = data.get('contact_info', organizer.contact_info)
        organizer.save()
        return JsonResponse({'organizer': model_to_dict(organizer)})
    except Organizer.DoesNotExist:
        return JsonResponse({'error': 'Organizer not found'}, status=404)

# Registro de Usuarios
@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    try:
        data = json.loads(request.body)
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
        
        role = data.get('role', 'user') 
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']), 
            role=role
        )
        return JsonResponse({'user': model_to_dict(user)}, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })