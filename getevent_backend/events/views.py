from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Ticket, Organizer  # Importamos Organizer
from django.forms.models import model_to_dict
import json

# Eventos
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

def event_detail(request, id):
    try:
        event = Event.objects.get(pk=id)
        return JsonResponse({'event': model_to_dict(event)})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@csrf_exempt
def event_create(request):
    if request.method == 'POST':
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
    return JsonResponse({'error': 'Invalid request method, use POST'}, status=405)

@csrf_exempt
def event_edit(request, id):
    try:
        event = Event.objects.get(pk=id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            event.name = data.get('name', event.name)
            event.date = data.get('date', event.date)
            event.location = data.get('location', event.location)
            event.description = data.get('description', event.description)
            event.is_private = data.get('is_private', event.is_private)
            event.password = data.get('password', event.password)
            event.save()
            return JsonResponse({'event': model_to_dict(event)})
        return JsonResponse({'error': 'Invalid request method, use PUT'}, status=405)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@csrf_exempt
def event_delete(request, id):
    try:
        event = Event.objects.get(pk=id)
        if request.method == 'DELETE':
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=204)
        return JsonResponse({'error': 'Invalid request method, use DELETE'}, status=405)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

# Tickets
def ticket_list(request, event_id):
    tickets = Ticket.objects.filter(event_id=event_id)
    ticket_data = [{'id': ticket.id, 'user': ticket.user.id, 'price': ticket.price} for ticket in tickets]
    return JsonResponse({'tickets': ticket_data})

def ticket_detail(request, event_id, ticket_id):
    try:
        ticket = Ticket.objects.get(event_id=event_id, pk=ticket_id)
        return JsonResponse({'ticket': model_to_dict(ticket)})
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)

@csrf_exempt
def ticket_create(request, event_id):
    if request.method == 'POST':
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
    return JsonResponse({'error': 'Invalid request method, use POST'}, status=405)

@csrf_exempt
def ticket_edit(request, event_id, ticket_id):
    try:
        ticket = Ticket.objects.get(event_id=event_id, pk=ticket_id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            ticket.price = data.get('price', ticket.price)
            ticket.is_active = data.get('is_active', ticket.is_active)
            ticket.save()
            return JsonResponse({'ticket': model_to_dict(ticket)})
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)

@csrf_exempt
def ticket_delete(request, event_id, ticket_id):
    try:
        ticket = Ticket.objects.get(event_id=event_id, pk=ticket_id)
        if request.method == 'DELETE':
            ticket.delete()
            return JsonResponse({'message': 'Ticket deleted successfully'}, status=204)
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)

# Organizadores
def organizer_list(request):
    organizers = Organizer.objects.all()
    organizer_data = [{'id': organizer.id, 'name': organizer.name, 'contact_info': organizer.contact_info} for organizer in organizers]
    return JsonResponse({'organizers': organizer_data})

def organizer_detail(request, id):
    try:
        organizer = Organizer.objects.get(pk=id)
        return JsonResponse({'organizer': model_to_dict(organizer)})
    except Organizer.DoesNotExist:
        return JsonResponse({'error': 'Organizer not found'}, status=404)

@csrf_exempt
def organizer_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            organizer = Organizer.objects.create(
                name=data['name'],
                contact_info=data['contact_info'],
                address=data.get('address', ''),
                description=data.get('description', ''),
                website=data.get('website', None)
            )
            return JsonResponse({'organizer': model_to_dict(organizer)}, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method, use POST'}, status=405)

@csrf_exempt
def organizer_edit(request, id):
    try:
        organizer = Organizer.objects.get(pk=id)
        if request.method == 'PUT':
            data = json.loads(request.body)
            organizer.name = data.get('name', organizer.name)
            organizer.contact_info = data.get('contact_info', organizer.contact_info)
            organizer.address = data.get('address', organizer.address)
            organizer.description = data.get('description', organizer.description)
            organizer.website = data.get('website', organizer.website)
            organizer.save()
            return JsonResponse({'organizer': model_to_dict(organizer)})
    except Organizer.DoesNotExist:
        return JsonResponse({'error': 'Organizer not found'}, status=404)

@csrf_exempt
def organizer_delete(request, id):
    try:
        organizer = Organizer.objects.get(pk=id)
        if request.method == 'DELETE':
            organizer.delete()
            return JsonResponse({'message': 'Organizer deleted successfully'}, status=204)
    except Organizer.DoesNotExist:
        return JsonResponse({'error': 'Organizer not found'}, status=404)