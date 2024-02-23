from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q
from .models import *
from .serializers import *
from .permissions import *


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    try:
        if not "email" in request.data or not "password" in request.data:
            return Response({"error": "email and password are required fields"}, status=status.HTTP_404_NOT_FOUND)
        if not request.data["email"] or not request.data["password"]:
            return Response({"error": "email and password cannot be blank or empty"}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(email=request.data["email"], password=request.data["password"])
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def signout(request):
    logout(request)
    return Response({"message": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)

class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            queryset = User.objects.get(id=id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            queryset = Content.objects.get(id=id)
            serializer = ContentSerializer(queryset)
            return Response(serializer.data)
        queryset = Content.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(summary__icontains=query) |
                Q(categories__name__icontains=query)
            )
        serializer = ContentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        content = Content.objects.get(id=id)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        content = Content.objects.get(id=id)
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
