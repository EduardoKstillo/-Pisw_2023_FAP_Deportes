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
    path("partner/", views.partner, name='partner'),    
    path("create_partner/", views.create_partner, name='create_partner'),
    path("detail_partner/<int:id>/", views.detail_partner, name='detail_partner'),
    path("edit_partner/<int:id>/", views.edit_partner, name='edit_partner'),
    path("delete_partner/<int:id>/", views.delete_partner, name='delete_partner'),
    path("details_partner/<int:id>/",
         views.details_partner, name='details_partner'),
]
