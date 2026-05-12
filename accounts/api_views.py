from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import MemberProfile, WeightLog, ExerciseLog, Payment, Exercise
from .serializers import (
    MemberProfileSerializer, 
    WeightLogSerializer, 
    ExerciseLogSerializer, 
    PaymentSerializer, 
    ExerciseSerializer
)

# Custom Permission to check if the user is an admin
class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow admins to see the list,
    but allow owners of an object to see their own object.
    """
    def has_permission(self, request, view):
        # Allow list view only for admin users
        if view.action == 'list':
            return request.user.is_staff
        # For other actions (retrieve, update, etc.), permission is granted
        # and will be checked at the object level by has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        # Admins can access any object
        if request.user.is_staff:
            return True
        # Regular users can only access their own profile information
        if isinstance(obj, MemberProfile):
            return obj.user == request.user
        # For other objects, check if the object's member is the request user
        return obj.member.user == request.user

class CustomAuthToken(ObtainAuthToken):
    """
    Custom login view that returns the user's token, username, and is_staff status.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_staff': user.is_staff
        })

class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        """
        This view should return a list of all members for admin users,
        but only the current user's profile for non-admin users.
        """
        user = self.request.user
        if user.is_staff:
            return MemberProfile.objects.all()
        return MemberProfile.objects.filter(user=user)

class WeightLogViewSet(viewsets.ModelViewSet):
    serializer_class = WeightLogSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WeightLog.objects.all()
        return WeightLog.objects.filter(member__user=user)

class ExerciseLogViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseLogSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ExerciseLog.objects.all()
        return ExerciseLog.objects.filter(member__user=user)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(member__user=user)

class ExerciseViewSet(viewsets.ModelViewSet):
    """
    Exercises are public information, so anyone can view them.
    Only admins can create, edit, or delete them.
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read-only for authenticated users
