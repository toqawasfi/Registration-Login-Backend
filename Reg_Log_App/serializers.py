import re
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    This serializer is used for user registration, validating and saving user data.
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    email = serializers.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        """
        Custom validation for the password field.

        Ensures that the password is at least 8 characters long and contains at least one uppercase letter.

        Args:
        - password: The user's password.

        Returns:
        - The validated password if it meets the criteria.

        Raises:
        - serializers.ValidationError if the password is invalid.
        """
        if len(password) < 8 or not re.search(r'[A-Z]', password):
            raise serializers.ValidationError(
                
            )
        return password

    def save(self):
        """
        Save method for user registration.

        Creates a new user account with the provided data.

        Returns:
        - The user account that has been created.

        Raises:
        - serializers.ValidationError if the passwords don't match or if the email is already in use.
        """
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords do not match. Please make sure both passwords match.'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email is already in use'})


        account = User(username=self.validated_data['username'], email=self.validated_data['email'])
        account.set_password(password)
        account.save()
        return account


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset.
    This serializer is used for password reset requests.
   """
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
