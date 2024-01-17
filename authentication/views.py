from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from .serializers import CustomAuthTokenSerializer, UserProfileSerializer, UserSerializer

from .models import UserProfile

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth import get_user_model

from .helpers import check_email, is_valid_password



User = get_user_model()


# ------------------------------- Home views -----------------------------------
class HomeAPIAuthViewList(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Reyvers Kitchen Auth service API"})


class CustomAuthToken(APIView):
    throttle_classes = []
    permission_classes = []
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = CustomAuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Change user token once requests are made continually
        oldTokens = Token.objects.filter(user__id=user.id)
        for token in oldTokens:
            token.delete()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# USER LOGOUT VIEW
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logoutView(request):
    # Check if the Authorization header is present in the request
    if 'Authorization' in request.headers:
        # Extract the token from the Authorization header
        auth_header = request.headers['Authorization']
        _, token = auth_header.split()  # Assuming the token is separated by a space after "Token"
        
        # Check if the token exists in the database
        try:
            user_token = Token.objects.get(key=token)
            user_token.delete()
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)



def get_user_from_token(request):
    # Check if the Authorization header is present in the request
    if 'Authorization' in request.headers:
        # Extract the token from the Authorization header
        auth_header = request.headers['Authorization']
        _, token = auth_header.split()  # Assuming the token is separated by a space after "Token"
        if token:
            token = Token.objects.get(key=token)
            return token.user
        else:
            return None
    else:
        return None


# USER PROFILE
@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    if request.method == 'GET':
        user = get_user_from_token(request)
        if user:
            userData = {
                "email": user.email,
                "name": user.profile.name,
                "date_of_birth": user.profile.date_of_birth,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
                "profile_picture": user.profile.get_image_url,
                "bio": user.profile.bio,
            }
            return Response(userData, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authorization header not found in the request."}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile was not  found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({"message": "Http Method not allowed."}, status=status.HTTP_400_BAD_REQUEST)
                                


@api_view(['POST'])
def create_new_user(request):
    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        if not email:
            return Response({
                "email": [
                    "This field may not be blank."
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({
                "password": [
                    "This field may not be blank."
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check if email and password are valid entry
            email_valid_status = check_email(email)
            password_valid_status = is_valid_password(password)
            if email_valid_status.status == False:
                return Response({
                    "email": [
                        error_message for error_message in email_valid_status.error_messages
                    ]
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if password_valid_status.status == False:
                return Response({
                    "password": [
                        error_message for error_message in password_valid_status.error_messages
                    ]
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Lastly Check if user already exists
            existing_user = User.objects.filter(email=email)
            if len(existing_user) > 1 or existing_user:
                return Response({
                    "email": [
                        "User with email already exists."
                    ]
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Finally create user Create user
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = User.objects.create_user(email=email, password=password)
                    user_details = {
                        "user_id": user.id,
                        "email": user.email,
                        "token": user.auth_token.key,
                    }
                    if user:
                        return Response(user_details, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({ "detail": "Http method not allowed." })

    






