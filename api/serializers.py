from rest_framework import serializers
from .models import User, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            email=validated_data.get('email', '')
        )
        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'name', 'phone_number', 'is_spam']  # Include all fields in the serializer
        extra_kwargs = {
            'user': {'required': False},  # Make user optional
            'name': {'required': False},  # Make name optional
            'phone_number': {'required': False},  # Make phone_number optional
        }

    def update(self, instance, validated_data):
        # Only update the 'is_spam' field if it's included in the request
        if 'is_spam' in validated_data:
            instance.is_spam = validated_data['is_spam']
        instance.save()
        return instance