from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path("users/", views.users, name='users'),
    path("create_user/", views.create_user, name='create_user'),
    path("edit_user/<int:id>/", views.edit_user, name='edit_user'),
    path("delete_user/<int:id>/", views.delete_user, name='delete_user'),
    path("denied/", views.denied, name='denied'),
]
