from Reg_Log_App.serializers import RegistrationSerializer,PasswordResetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Reg_Log_App import models
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail



@api_view(['POST'])
def registration_view(request):
    """
    Register a new user.
    
    This view allows users to register by providing their information via a POST request.

    Parameters:
    - request: HTTP request object containing user registration data.

    Returns:
    - HTTP response with registration success or error message.

    HTTP Methods:
    - POST
    """
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            response_data = {
                'message': 'Registration Successful!',
                'username': account.username,
                'email': account.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            

            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    """
     Logout the user by deleting their authentication token.

    This view allows users to log out by providing their authentication token in the request header.

    Parameters:
    - request: HTTP request object containing the authentication token in the 'Authorization' header.

    Returns:
    - HTTP response with a success message or an error message.

    HTTP Methods:
    - POST
    """
    if request.method == 'POST':
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is not None and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                tokens_to_delete = Token.objects.filter(key=token_key)
                tokens_to_delete.delete()
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'message': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)




@api_view(['POST'])
def send_email(request):
    """
    Send a password reset email to the user.

    This view allows users to request a password reset email. Upon successful request,
    an email with a password reset link is sent to the user's email address.

    Parameters:
    - request: HTTP request object containing the user's username and email.

    Returns:
    - HTTP response with a success message and the password reset link, or an error message.

    HTTP Methods:
    - POST
  """

  
    if request.method == 'POST':
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            reset_link = "http://localhost:3000/password_reset"
            subject = 'Password Reset Request'
            message = f'Hello {username}, please click the link below to reset your password:\n\n{reset_link}'
            from_email = 'toqatask@gmail.com'  
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return JsonResponse({'message': 'Password reset link generated successfully.', 'reset_link': reset_link}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_reset(request):
    """
    Reset the user's password.

    This view allows users to reset their password by providing their username, email, and a new password.

    Parameters:
    - request: HTTP request object containing the user's username, email, and new password.

    Returns:
    - HTTP response with a success message or an error message.

    HTTP Methods:
    - POST
    """
   
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        if len(new_password) < 8 or not any(c.isupper() for c in new_password):
            return Response({'message': 'Password must be at least 8 characters long and contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Enter your new password.'}, status=status.HTTP_200_OK)
