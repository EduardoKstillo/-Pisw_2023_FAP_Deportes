from django.urls import path
from . import views

urlpatterns = [
    path("", views.championships, name='championships'),
    path("categorys/", views.categorys, name='categorys'),
    path("create_category/", views.create_category, name='create_category'),
    path("create_championship/", views.create_championship,
         name='create_championship'),
    path("view_championship/<int:id_champ>/",
         views.view_championship, name='view_championship'),
    path("teams/<int:id_champ>/", views.teams, name='teams'),
    path("create_team/<int:id_champ>/", views.create_team, name='create_team'),
    path("players/<int:id_team>/<int:id_champ>/", views.players, name='players'),
    path("create_player/<int:id_team>/<int:id_champ>/",
         views.create_player, name='create_player'),
    path("fixture/<int:id_champ>", views.fixture, name='fixture'),
    path("create_fixture/<int:id_champ>",
         views.create_fixture, name='create_fixture'),
    path("games/<int:id_champ>", views.games, name='games'),
]
