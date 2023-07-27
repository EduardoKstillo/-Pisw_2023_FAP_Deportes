from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Championship, Team, Player, Game
from .forms import CategoryForm, ChampionshipForm, TeamForm, PlayerForm
from .filters import TeamFilter
from .fixture import generate_fixture, print_fixture
from django.http import HttpResponse
from django.contrib import messages


def categorys(request):
    categorys = Category.objects.all()
    context = {'categorys': categorys}
    return render(request, 'championship/category/categorys.html', context)


def create_category(request):
    if request.method == 'GET':
        context = {'form': CategoryForm}
        return render(request, 'championship/category/create_category.html', context)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorys')


def championships(request):
    championships = Championship.objects.all()
    context = {'championships': championships}
    return render(request, 'championship/championship/championship.html', context)


def create_championship(request):
    if request.method == 'GET':
        context = {'form': ChampionshipForm}
        return render(request, 'championship/championship/create_championship.html', context)

    if request.method == 'POST':
        form = ChampionshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('championships')


def view_championship(request, id_champ):
    championship = Championship.objects.get(id=id_champ)
    context = {'championship': championship}
    return render(request, 'championship/championship/view_championship.html', context)


def teams(request, id_champ):

    championship = Championship.objects.get(id=id_champ)
    teams = championship.teams.all()
    myfilter = TeamFilter(request.GET, queryset=teams)
    teams = myfilter.qs
    context = {'teams': teams, 'id_champ': championship.id, 'filter': myfilter}
    return render(request, 'championship/team/teams.html', context)


def create_team(request, id_champ):

    if request.method == 'GET':
        championship = Championship.objects.get(id=id_champ)
        # categorys = championship.categorys.all()   #enviar en el context
        context = {'form': TeamForm, 'id_champ': id_champ}

        return render(request, 'championship/team/create_team.html', context)

    if request.method == 'POST':
        championship = Championship.objects.get(id=id_champ)
        form = TeamForm(request.POST)
        if form.is_valid():
            team = Team.objects.create(
                name=request.POST['name'], category=request.POST['category'])
            team.save()
            championship.teams.add(team)
        return redirect('teams', id_champ)


def players(request, id_team, id_champ):
    team = Team.objects.get(id=id_team)
    players = team.players.all()
    context = {'players': players,
               'id_team': id_team,
               'id_champ': id_champ}
    return render(request, 'championship/player/players.html', context)


def create_player(request, id_team, id_champ):
    if request.method == 'GET':
        context = {'form': PlayerForm}
        return render(request, 'championship/player/create_player.html', context)
    if request.method == 'POST':
        team = Team.objects.get(id=id_team)
        player = Player.objects.create(
            name=request.POST['name'], surnames=request.POST['surnames'])
        player.save()
        team.players.add(player)

        return redirect('players', id_team, id_champ)


def fixture(request, id_champ):

    championship = get_object_or_404(Championship, pk=id_champ)
    fixtures = Game.objects.filter(
        championship=championship).order_by('round_number')
    grouped_fixtures = {}
    for fixture in fixtures:
        round_number = fixture.round_number
        if round_number not in grouped_fixtures:
            grouped_fixtures[round_number] = []
        grouped_fixtures[round_number].append(fixture)

    return render(request, 'championship/fixture.html', {'grouped_fixtures': grouped_fixtures, 'id_champ': id_champ})


def create_fixture(request, id_champ):

    championship = get_object_or_404(Championship, pk=id_champ)
    print(championship)

    # Verificar si ya existe un fixture para el campeonato
    existing_fixture = Game.objects.filter(championship=championship)
    if existing_fixture.exists():
        print(existing_fixture)
        messages.success(request, 'El fixture ya esta creado!')
        return redirect('fixture', id_champ)

    teams = championship.teams.all()
    fixture = generate_fixture(teams, championship)
    return redirect('fixture', id_champ)


def games(request, id_champ):
    championship = get_object_or_404(Championship, pk=id_champ)
    fixtures = Game.objects.filter(
        championship=championship).order_by('round_number')
    grouped_fixtures = {}
    for fixture in fixtures:
        round_number = fixture.round_number
        if round_number not in grouped_fixtures:
            grouped_fixtures[round_number] = []
        grouped_fixtures[round_number].append(fixture)
    # print(fixture)
    # print_fixture(fixture)
    return render(request, 'championship/games.html', {'grouped_fixtures': grouped_fixtures, 'id_champ': id_champ})


"""
revisar las urls
optimizar urls
falta editar, eliminar y validar
bloquear creacion de equipos cuando se genere el fixture
falta opcion de eliminar fixture
"""
