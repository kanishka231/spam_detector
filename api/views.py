import logging
from django.forms import ValidationError
from rest_framework import generics, permissions, status
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Ensure phone number is unique
        phone_number = serializer.validated_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({"error": "Phone number already registered"})
        serializer.save()

class SearchByNameView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Contact.objects.filter(Q(name__istartswith=query) | Q(name__icontains=query))

class SearchByPhoneView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        phone = self.request.query_params.get('phone', '')
        return Contact.objects.filter(phone_number=phone)

class MarkSpamView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_update(self, serializer):
        # Only update the 'is_spam' field
        serializer.save(is_spam=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'partial': True})  # Ensure partial updates are allowed
        return context

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        # Check if user exists using phone number
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                logger.info(f"Token generated: {token.key}")
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                raise ValueError("Incorrect password")
        except User.DoesNotExist:
            logger.warning(f"Invalid credentials for phone number: {phone_number}")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

