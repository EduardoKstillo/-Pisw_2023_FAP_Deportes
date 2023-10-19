from django.urls import path
from . import views

urlpatterns = [
    path("", views.championships, name="championships"),
    path("categorys/", views.categorys, name="categorys"),
    path("create_category/", views.create_category, name="create_category"),
    path("delete_championship/<int:id>/",views.delete_championship,name="delete_championship"),
    path("teams/", views.teams, name='teams'),
    path("create_team/", views.create_team, name='create_team'),
    path("delete_team/<int:id>/<int:id_champ>/", views.delete_team, name="delete_team"),
    path("players/<int:id_team>/<int:id_champ>/", views.players, name="players"),
    path(
        "create_player/<int:id_team>/<int:id_champ>/",
        views.create_player,
        name="create_player",
    ),
    path(
        "delete_player/<int:id>/<int:id_team>/<int:id_champ>/",
        views.delete_player,
        name="delete_player",
    ),
    path("fixture/<int:id_champ>", views.fixture, name="fixture"),
    path("create_fixture/<int:id_champ>", views.create_fixture, name="create_fixture"),
    path("games/<int:id_champ>", views.games, name="games"),
    path("details_player/<int:id>/",
         views.details_player, name='details_player'),
    path("edit_player/<int:id>/<int:id_team>/<int:id_champ>/", 
         views.edit_player, name='edit_player'),
    path("edit_team/<int:id>/<int:id_champ>/", 
         views.edit_team, name='edit_team'),
    path("delete_team/<int:id>/<int:id_champ>/",views.delete_team, name='delete_team'),
    path('add_player_team/<int:player_id>/', views.add__player_team, name='add_player_team'), 
    path('view_team/<int:team_id>/', views.view_team, name='view_team'),
    path('create_person/', views.create_person, name='create_person'),
    path('persons/', views.persons, name='persons'),
    path('view_person/<int:person_id>/', views.view_person, name='view_person'),
    path('add_team_championship/<int:championship_id>/', views.add_team_championship, name='add_team_championship'),
    path('view1_championship/<int:championship_id>/', views.view1_championship, name='view1_championship'),
    path("create_championship/", views.create_championship,name='create_championship'),
    path('remove_player_from_team/<int:team_id>/<int:player_id>/', views.remove_player_from_team, name='remove_player_from_team'),
]
