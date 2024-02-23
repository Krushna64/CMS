from django.urls import path
from .views import *


urlpatterns = [
    # Auth
    path('login', signin, name='login'),
    path('logout', signout, name='logout'),
    # User
    # path('users', UserListCreateView.as_view(), name='user-list-create'),
    # path('users/<int:id>', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('users', UserAPI.as_view(), name='user-list-create'),
    path('users/<int:id>', UserAPI.as_view(), name='user-retrieve-update-destroy'),
    # Contents
    path('contents', ContentAPI.as_view(), name='content-list-create'),
    path('contents/<int:id>', ContentAPI.as_view(), name='content-retrieve-update-destroy'),
]