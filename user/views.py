from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken    
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from datetime import timedelta
from django.db.models import Q
from django.utils import timezone

from .models import User, FriendRequest
from .serializers import TokenSerializer,CustomTokenRefreshSerializer,RegisterSerializer,UserSerializer,FriendRequestSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    """ View for user login """
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Custom Refresh token View"""
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    """View to logout """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.POST.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": 'Logout Success.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(generics.ListAPIView):
    """ User Search """
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q', '')
        if '@' in search_keyword:
            # Exact email match
            return User.objects.filter(email=search_keyword).exclude(is_superuser=True) 
        else:
            # Partial name match
            return User.objects.filter(username__icontains=search_keyword).exclude(is_superuser=True) 

class FriendRequestAPIView(generics.CreateAPIView):
    """ Create friend request """
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = request.data.get('to_user')
        # Check if the sender has sent more than 3 requests within the last minute
        recent_requests = FriendRequest.objects.filter(from_user=sender, created__gte=timezone.now() - timedelta(minutes=1)).count()
        if recent_requests >= 3:
            return Response({"error": "You cannot send more than 3 friend requests within a minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Check if the receiver exists
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the sender has already sent a friend request to the receiver
        existing_request = FriendRequest.objects.filter(from_user=sender, to_user=receiver)
        if existing_request.exists():
            return Response({"error": "Friend request already sent to this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the friend request
        friend_request = FriendRequest.objects.create(from_user=sender, to_user=receiver, status=FriendRequest.REQUESTED)
        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AcceptFriendRequestAPIView(generics.UpdateAPIView):
    """ Accept friend request """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user == request.user and instance.status == FriendRequest.REQUESTED:
            instance.status = FriendRequest.ACCEPTED
            instance.save()
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to accept this friend request."}, status=status.HTTP_403_FORBIDDEN)

class RejectFriendRequestAPIView(generics.UpdateAPIView):
    """ Reject friend request """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user == request.user and instance.status == FriendRequest.REQUESTED:
            instance.status = FriendRequest.REJECTED
            instance.save()
            return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not authorized to reject this friend request."}, status=status.HTTP_403_FORBIDDEN)
      
class FriendListAPIView(generics.ListAPIView):
    """ List friends and reject friend requests"""
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = FriendRequest.objects
        status = self.request.query_params.get('status', '')
        if status == 'pending':
            query = query.filter(to_user=self.request.user, status=FriendRequest.REQUESTED)
        else:
            query = query.filter(Q(to_user=self.request.user)|Q(from_user=self.request.user), status=FriendRequest.ACCEPTED)
        return query
