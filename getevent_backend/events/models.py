from django.db import models
from django.contrib.auth.models import AbstractUser

# Model for User with role field
class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('organizer', 'Organizer'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # Nuevo campo para definir el rol

    def __str__(self):
        return f"{self.username} ({self.role})"

# Model for Organizer
class Organizer(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()  # Puede incluir email, teléfono, etc.
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Model for Event
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=5, blank=True, null=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.SET_NULL, null=True, related_name='events')

    def __str__(self):
        return self.name

# Model for Venue
class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Model for Ticket
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Ticket for {self.event.name} by {self.user.username}"