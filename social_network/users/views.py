from .serializers import RegisterSerializer, FriendRequestSerializer, UserSerializer, FriendSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from datetime import timedelta
from django.utils import timezone
from .models import FriendRequest, User
from django.db.models import Q
from rest_framework import generics


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = SearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if not query:
            return User.objects.none()

        query = query.strip()
        users_by_email = User.objects.filter(email__iexact=query)
        if users_by_email.exists():
            return users_by_email

        users_by_name = User.objects.filter(username__icontains=query)
        return users_by_name

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'count': self.paginator.page.paginator.count,
                'page_size': self.paginator.page_size,
                'current_page': self.paginator.page.number,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
            },
            'success': True,
            'message': 'Search results retrieved successfully.',
            'results': data
        })


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        receiver_id = request.data.get('receiver_id')

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(sender=request.user, timestamp__gte=one_minute_ago)
        if recent_requests.count() >= 3:
            return Response({"detail": "Cannot send more than 3 friend requests within a minute."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver)
        serializer = FriendRequestSerializer(friend_request)

        response_data = {
            "detail": "Friend request sent successfully.",
            "friend_request": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class RespondToFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')

        try:
            friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        sender_username = friend_request.sender.username

        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({"detail": f"Friend request from {sender_username} accepted."}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"detail": f"Friend request from {sender_username} rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        friends = User.objects.filter(
            Q(sent_requests__receiver=request.user, sent_requests__status='accepted') |
            Q(received_requests__sender=request.user, received_requests__status='accepted')
        ).distinct()

        serializer = FriendSerializer(friends, many=True)
        response_data = {
            "detail": "Friends list retrieved successfully.",
            "friends": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ListPendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
        print('data', request.user)
        serializer = FriendRequestSerializer(pending_requests, many=True)

        response_data = {
            "detail": "Pending friend requests retrieved successfully.",
            "count": pending_requests.count(),
            "pending_requests": serializer.data
        }
        print("serializer.data",serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)




