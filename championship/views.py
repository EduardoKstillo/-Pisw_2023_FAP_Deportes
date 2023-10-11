from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Championship, Team, Player, Game, Person
from .forms import CategoryForm, ChampionshipForm, TeamForm, PlayerForm, PersonForm
from .filters import TeamFilter
from .fixture import generate_fixture, print_fixture
from django.http import HttpResponse
from django.contrib import messages



def categorys(request):
    categorys = Category.objects.all()
    context = {"categorys": categorys}
    return render(request, "championship/category/categorys.html", context)


def create_category(request):
    if request.method == "GET":
        context = {"form": CategoryForm}
        return render(request, "championship/category/create_category.html", context)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categorys")


def championships(request):
    championships = Championship.objects.all()
    context = {"championships": championships}
    return render(request, "championship/championship/championship.html", context)


def create_championship(request):
    if request.method == 'POST':
        form = ChampionshipForm(request.POST)
        if form.is_valid():
            form.save()
            print("Formulario válido, redirigiendo...")
            return redirect('championships')  # Cambia 'lista_campeonatos' por el nombre de tu vista de lista de campeonatos
    else:
        form = ChampionshipForm()
    return render(request, 'championship/championship/create_championship.html', {'form': form})



def delete_championship(request, id):
    championship = get_object_or_404(Championship, pk=id)
    championship.delete()
    return redirect("championships")




def teams(request):

    teams=Team.objects.all()
    return render(request,'championship/team/teams.html',{'teams':teams})

def create_team(request):

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teams')  # Cambia 'lista_campeonatos' por el nombre de tu vista de lista de campeonatos
    else:
        form = TeamForm()
    return render(request, 'championship/Team/create_team.html', {'form': form})

def view_team(request, team_id):
    team = Team.objects.get(id=team_id)
    teams = team.Persons.all()
    return render(request, 'championship/team/view_team.html', {'team': team, 'players': teams})

def delete_team(request, id, id_champ):
    team = get_object_or_404(Team, pk=id)
    team.delete()
    return redirect(request, 'teams', id_champ)

def add__player_team(request, player_id):
    team = Team.objects.get(pk=player_id)
    players_available = Person.objects.exclude(team=team)  # Obtener personas que no están en el equipo

    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Person.objects.get(pk=player_id)
        team.Persons.add(player)  # Agregar la persona al equipo
        
    return render(request, 'championship/team/add_player_team.html', {'team': team, 'players':players_available})


def players(request, id_team, id_champ):
    team = Team.objects.get(id=id_team)
    players = team.players.all()
    context = {"players": players, "id_team": id_team, "id_champ": id_champ}
    return render(request, "championship/player/players.html", context)


def create_player(request, id_team, id_champ):
    if request.method == "GET":
        context = {"form": PlayerForm}
        return render(request, "championship/player/create_player.html", context)
    if request.method == "POST":
        team = Team.objects.get(id=id_team)
        player = Player.objects.create(
            name=request.POST["name"], surnames=request.POST["surnames"]
        )
        player.save()
        team.players.add(player)

        return redirect("players", id_team, id_champ)


def delete_player(request, id, id_team, id_champ):
    player = get_object_or_404(Player, pk=id)
    player.delete()
    return redirect("players", id_team, id_champ)


def fixture(request, id_champ):
    championship = get_object_or_404(Championship, pk=id_champ)
    fixtures = Game.objects.filter(championship=championship).order_by("round_number")
    grouped_fixtures = {}
    for fixture in fixtures:
        round_number = fixture.round_number
        if round_number not in grouped_fixtures:
            grouped_fixtures[round_number] = []
        grouped_fixtures[round_number].append(fixture)

    return render(
        request,
        "championship/fixture.html",
        {"grouped_fixtures": grouped_fixtures, "id_champ": id_champ},
    )


def create_fixture(request, id_champ):
    championship = get_object_or_404(Championship, pk=id_champ)
    print(championship)

    # Verificar si ya existe un fixture para el campeonato
    existing_fixture = Game.objects.filter(championship=championship)
    if existing_fixture.exists():
        print(existing_fixture)
        messages.success(request, "El fixture ya esta creado!")
        return redirect("fixture", id_champ)

    teams = championship.teams.all()
    fixture = generate_fixture(teams, championship)
    return redirect("fixture", id_champ)


def games(request, id_champ):
    championship = get_object_or_404(Championship, pk=id_champ)
    fixtures = Game.objects.filter(championship=championship).order_by("round_number")
    grouped_fixtures = {}
    for fixture in fixtures:
        round_number = fixture.round_number
        if round_number not in grouped_fixtures:
            grouped_fixtures[round_number] = []
        grouped_fixtures[round_number].append(fixture)
    # print(fixture)
    # print_fixture(fixture)
    return render(
        request,
        "championship/games.html",
        {"grouped_fixtures": grouped_fixtures, "id_champ": id_champ},
    )
def details_player(request, id):
    player = get_object_or_404(Player, pk=id)

    if request.method == 'GET':
        form = PlayerForm(instance=player)
        context = {'form': form}
        return render(request, 'championship/player/details_player.html', context)

def edit_player(request, id, id_team, id_champ):
    player = get_object_or_404(Player, pk=id)

    if request.method == 'GET':
        form = PlayerForm(instance=player)
        context = {'form': form, 'player': player}
        return render(request, 'championship/player/edit_player.html', context)

    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jugador editado correctamente!')
            return redirect('players', id_team, id_champ)
        else:
            messages.success(request, 'Ingrese los datos correctamente')
            return render(request, 'championship/player/create_player.html', {'form': form})

def edit_team(request, id, id_champ):
    team = get_object_or_404(Team, pk=id)

    if request.method == 'GET':
        form = TeamForm(instance=team)
        context = {'form': form, 'team': team}
        return render(request, 'championship/team/edit_team.html', context)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipo editado correctamente!')
            return redirect('teams', id_champ)
        else:
            messages.success(request, 'Ingrese los datos correctamente')
            return render(request, 'championship/team/create_team.html', {'form': form})

#------------------------------
def persons(request):
    persons=Person.objects.all()
    return render(request,'championship/person/persons.html',{'persons':persons})

def create_person(request):
    if request.method == 'GET':
        form = PersonForm
        context = {'form': form}
        return render(request, 'championship/person/create_person.html', context)
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'persona creado correctamente!')
            return redirect('teams')
        else:
            messages.success(request, 'Ingrese los datos correctamente')
            return render(request, 'championship/person/create_person.html', {'form': form})
        # return redirect('home')

def view_person(request, person_id):
    person = Person.objects.get(id=person_id)
    context = {'person': person}
    return render(request, 'championship/person/view_person.html', context)

def delete_person(request, id):
    person = get_object_or_404(Person, pk=id)
    person.delete()
    return redirect(request, 'persons')

#----------------------------------
def add_team_championship(request, championship_id):
    championship = Championship.objects.get(pk=championship_id)
    teams_availables = Team.objects.exclude(championship=championship)

    if request.method == 'POST':
        # Si el formulario se envió, procesa los datos aquí.
        teams_id = request.POST.get('championship_id')
        team_id = Team.objects.get(pk=teams_id)
        championship.teams.add(team_id)
        #campeonato.save()
        return redirect('teams')

    #equipos_disponibles = Team.objects.all()
    return render(request, 'championship/championship/add_team_championship.html', {'championship': championship, 'teams': teams_availables})

def view_championship(request, id_champ):
    championship = Championship.objects.get(id=id_champ)
    context = {'championship': championship}
    return render(request, 'championship/championship/view_championship.html', context)



"""
revisar las urls
optimizar urls
falta editar, eliminar y validar
bloquear creacion de equipos cuando se genere el fixture
falta opcion de eliminar fixture
"""
