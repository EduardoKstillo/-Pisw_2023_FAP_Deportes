from django.urls import path
from . import views

urlpatterns = [
    path("", views.championships, name="championships"),
    path("categorys/", views.categorys, name="categorys"),
    path("create_category/", views.create_category, name="create_category"),
    path(
        "delete_championship/<int:id>/",
        views.delete_championship,
        name="delete_championship",
    ),
    path("teams/", views.teams, name="teams"),
    path("create_team/", views.create_team, name="create_team"),
    # path("delete_team1/<int:id>/<int:id_champ>/", views.delete_team, name="delete_team"),

    path("create_fixture/<int:championship_id>/<int:category_id>/", views.create_fixture, name="create_fixture"),
    path("game/<int:game_id>/", views.game, name="game"),
    path('game_status/<int:game_id>/', views.game_status, name='game_status'),


    path("delete_team/<int:id>/<int:id_champ>/", views.delete_team, name="delete_team"),
    # path('add_player_team/<int:player_id>/', views.add__player_team, name='add_player_team'),
    path("view_team/<int:team_id>/", views.view_team, name="view_team"),
    path("persons/", views.persons, name="persons"),  # Person
    path("create_person/", views.create_person, name="create_person"),  # Person
    path(
        "edit_person/<int:person_id>/", views.edit_person, name="edit_person"
    ),  # Person
    path(
        "view_person/<int:person_id>/", views.view_person, name="view_person"
    ),  # Person
    path(
        "delete_person/<int:person_id>/", views.delete_person, name="delete_person"
    ),  # Person
    #path("add_team_championship/<int:championship_id>/",views.add_team_championship,name="add_team_championship",),
    # path('view1_championship/<int:championship_id>/', views.view1_championship, name='view1_championship'),
    path("create_championship/", views.create_championship, name="create_championship"),
    path(
        "remove_player_from_team/<int:team_id>/<int:player_id>/",
        views.remove_player_from_team,
        name="remove_player_from_team",
    ),
    path("delete_team/<int:team_id>/", views.delete_team, name="delete_team"),
    path(
        "remove_team_from_championship/<int:championship_id>/<int:category_id>/<int:team_id>/",
        views.remove_team_from_championship,
        name="remove_team_from_championship",
    ),
    path(
        "delete_category/<int:category_id>/",
        views.delete_category,
        name="delete_category",
    ),
    path("edit_category/<int:category_id>/", views.edit_category, name="edit_category"),
    path(
        "edit_championship/<int:championship_id>",
        views.edit_championship,
        name="edit_championship",
    ),
    path("edit_team/<int:team_id>", views.edit_team, name="edit_team"),
    path("view_championship/<int:championship_id>", views.view_championship, name="view_championship"),
    path("add_team_championship/<int:championship_id>/<int:categorys_id>/",views.add_team_championship,name="add_team_championship"),
    #--Creacion de los nuevos modelos disciplina
    path("disciplines/", views.disciplines, name="disciplines"),
    path("create_discipline/", views.create_discipline, name="create_discipline"),
    path("delete_discipline/<int:discipline_id>/",views.delete_discipline,name="delete_discipline",),
    path("edit_discipline/<int:discipline_id>/", views.edit_discipline, name="edit_discipline"),
    #--Creacopm del modelo temporada
    path("seasons/", views.seasons, name="seasons"),
    path("create_season/", views.create_season, name="create_season"),
    path("delete_season/<int:season_id>/",views.delete_season,name="delete_season",),
    path("edit_season/<int:season_id>/", views.edit_season, name="edit_season"),
    #--Actualizacion de la persona marcada como delegado del equipo
    path('actualizar_jugador/<int:player_id>/', views.actualizar_jugador, name='actualizar_jugador'),
    path('actualizar_jugador1/<int:player_id>/', views.actualizar_jugador1, name='actualizar_jugador1'),

    path('tabla_posiciones/<int:championship_id>/<int:category_id>/', views.tabla_posiciones, name='tabla_posiciones'),
    path('amonestaciones/<int:championship_id>/<int:category_id>/', views.amonestaciones, name='amonestaciones'),
    path('goleadores/<int:championship_id>/<int:category_id>/', views.goleadores, name='goleadores'),

    # Modulo anuncios
    path('anuncios/', views.anuncios,  name='anuncios'),
    path('denied/', views.denied,  name='denied'),
    path('create_anuncio/', views.create_anuncio,  name='create_anuncio'),

]
