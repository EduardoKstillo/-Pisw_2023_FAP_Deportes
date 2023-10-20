from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Championship, Team, Player, Game, Person
from .forms import CategoryForm, ChampionshipForm, TeamForm, PlayerForm, PersonForm
from .filters import TeamFilter
from .fixture import generate_fixture, print_fixture
from django.http import HttpResponse
from django.contrib import messages
from itertools import zip_longest


def categorys(request):
    categorys = Category.objects.all().order_by('name')
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
            return redirect('championships')
    else:
        form = ChampionshipForm()

    # Agrupa los campos en pares
    fields = form.visible_fields()
    grouped_fields = [fields[i:i+2] for i in range(0, len(fields), 2)]

    return render(request, 'championship/championship/create_championship.html', {'form': form, 'grouped_fields': grouped_fields})



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
            team_month = form.cleaned_data['month']
            team_year = form.cleaned_data['year']
            team_group = form.cleaned_data['group']
            if Team.objects.filter(month=team_month, year=team_year, group=team_group).exists():
                form.add_error('group', 'ya existe un equipo con dicho grupo')
            else:
                form.save()
                return redirect('teams')
    else:
        form = TeamForm()
    return render(request, 'championship/Team/create_team.html', {'form': form})

def view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = team.Persons.all()
    players_available = Person.objects.filter(team=None)

    # Calcula cuántas personas cumplen la condición y cuántas no
    cumplen_condicion = 0
    no_cumplen_condicion = 0

    for player in players:
        if player.month_promotion == team.month and player.year_promotion == team.year:
            cumplen_condicion += 1
        else:
            no_cumplen_condicion += 1

    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Person.objects.get(pk=player_id)

        # Verifica si se ha alcanzado el límite de 10 personas en el equipo
        if len(players) >= 4:
            messages.error(request, "El equipo ya tiene el máximo número de jugadores permitidos (10).")
        else:
            # Verifica si el jugador cumple la condición
            if player.month_promotion == team.month and player.year_promotion == team.year:
                cumplen_condicion += 1
            else:
                no_cumplen_condicion += 1

            # Verifica si se han agregado 7 personas que cumplen la condición
            if no_cumplen_condicion <= 2:
                team.Persons.add(player)
                #messages.success(request, "Jugador agregado exitosamente.")
                return redirect('view_team', team_id=team.id)
            else:
                messages.error(request, "No se pueden agregar más jugadores que no cumplen las condiciónes ")

    return render(request, 'championship/team/view_team.html', {
        'team': team,
        'players': players,
        'players_available': players_available,
    })

def remove_player_from_team(request, team_id, player_id):
    team = get_object_or_404(Team, pk=team_id)
    player = get_object_or_404(Person, pk=player_id)

    if request.method == 'POST':
        # Elimina al jugador del equipo
        team.Persons.remove(player)

    return redirect('view_team', team_id=team.id)

def remove_team_from_championship(request, championship_id, team_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        # Elimina al equipo del campeonato
        championship.teams.remove(team)

    return redirect('add_team_championship', championship_id=championship.id)

def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect('teams')

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('categorys')

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categorys')  # Reemplaza 'list_categories' con la URL de la vista que muestra todas las categorías.
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'championship/category/edit_category.html', {'form': form, 'category': category})

def edit_championship(request, championship_id):
    championship = get_object_or_404(Championship, pk=championship_id)

    if request.method == 'POST':
        form = ChampionshipForm(request.POST, instance=championship)
        if form.is_valid():
            form.save()
            print("Formulario válido, redirigiendo...")
            return redirect('championships')
    else:
        form = ChampionshipForm(instance=championship)

    # Agrupa los campos en pares
    fields = form.visible_fields()
    grouped_fields = [fields[i:i+2] for i in range(0, len(fields), 2)]

    context = {
        'form': form,
        'grouped_fields': grouped_fields,
        'championship': championship  # Add the championship instance to the context
    }

    return render(request, 'championship/championship/edit_championship.html', context)

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
"""
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
"""
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    form = TeamForm(instance=team)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)  # Pasa la instancia del equipo a editar
        if form.is_valid():
            team_month = form.cleaned_data['month']
            team_year = form.cleaned_data['year']
            team_group = form.cleaned_data['group']
            if Team.objects.filter(month=team_month, year=team_year, group=team_group).exclude(pk=team_id).exists():
                form.add_error('group', 'Ya existe un equipo con dicho grupo')
            else:
                form.save()
                return redirect('teams')
    else:
        form = TeamForm(instance=team)  # Pasa la instancia del equipo a editar

    context = {'form': form,'teams': team}

    return render(request, 'championship/team/edit_team.html', context)

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
            return redirect('persons')
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
    año_inicial = int(championship.categorys.name)  # Reemplaza con el año inicial deseado
    año_final = año_inicial+9   # Reemplaza con el año final deseado
    teams_availables = Team.objects.filter(year__gte=año_inicial, year__lte=año_final).exclude(championship=championship)

    if request.method == 'POST':
        # Si el formulario se envió, procesa los datos aquí.
        teams_id = request.POST.get('championship_id')
        team_id = Team.objects.get(pk=teams_id)
        championship.teams.add(team_id)
        #campeonato.save()
        return redirect('add_team_championship', championship_id=championship.id)

    #equipos_disponibles = Team.objects.all()
    return render(request, 'championship/championship/add_team_championship.html', {'championship': championship, 'teams': teams_availables})

def view_championship(request, id_champ):
    championship = Championship.objects.get(id=id_champ)
    context = {'championship': championship}
    return render(request, 'championship/championship/view_championship.html', context)

def view1_championship(request, championship_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            championship.teams.add(team)
            return redirect('championships')
            

    teams_availables = Team.objects.exclude(championship=championship)

    return render(request, 'championship/championship/view1_championship.html', {
        'championship': championship,
        'teams_availables': teams_availables,
    })



"""
revisar las urls
optimizar urls
falta editar, eliminar y validar
bloquear creacion de equipos cuando se genere el fixture
falta opcion de eliminar fixture
"""
