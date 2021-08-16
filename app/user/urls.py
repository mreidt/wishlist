from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path(
        'create/',
        views.CreateUserView.as_view(),
        name='create'),
    path(
        'token/',
        views.CreateTokenView.as_view(),
        name='token'),
    path(
        'me/',
        views.ManageUserView.as_view(),
        name='me'),
    path(
        'remove/',
        views.RemoveUserView.as_view(),
        name='remove'),
    path(
        'list/',
        views.ListUsersView.as_view(),
        name='list'),
    path(
        'create-superuser/',
        views.CreateSuperuserView.as_view(),
        name='create-superuser'),
]
