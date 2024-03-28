from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='auth_login'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path('search/', views.UserSearchAPIView.as_view(), name='user-search'),
    path('friend-request/', views.FriendRequestAPIView.as_view(), name='friend-request'),
    path('accept-friend-request/<int:pk>/', views.AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),
    path('reject-friend-request/<int:pk>/', views.RejectFriendRequestAPIView.as_view(), name='reject-friend-request'),
    path('friend-list/', views.FriendListAPIView.as_view(), name='friend-list'),

]
