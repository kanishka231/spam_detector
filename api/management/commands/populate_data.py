from django.core.management.base import BaseCommand
from api.models import User, Contact
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = [
            User(username=f'user{i}', phone_number=f'123456789{i}')
            for i in range(1, 11)
        ]
        User.objects.bulk_create(users)

        for user in User.objects.all():
            contacts = [
                Contact(user=user, name=f'Contact {i}', phone_number=f'987654321{i}')
                for i in range(1, 6)
            ]
            Contact.objects.bulk_create(contacts)
