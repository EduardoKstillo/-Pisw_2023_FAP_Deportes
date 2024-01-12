from django.contrib import admin
from .models import Category, Championship, Team, Person, Game, PlayerGame, Result, Anuncio

admin.site.register(Category)
admin.site.register(Championship)
admin.site.register(Team)
admin.site.register(Person)
admin.site.register(Game)
admin.site.register(PlayerGame)
admin.site.register(Result)
admin.site.register(Anuncio)
