from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, SearchUserView, SendFriendRequestView,
    RespondToFriendRequestView, ListFriendsView, ListPendingRequestsView
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', SearchUserView.as_view(), name='search_user'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/respond/', RespondToFriendRequestView.as_view(), name='respond_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend-requests/pending/', ListPendingRequestsView.as_view(), name='list_pending_requests'),
]
