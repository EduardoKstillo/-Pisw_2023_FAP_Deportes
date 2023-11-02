from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Championship, Team, Player, Game, Person
from .forms import CategoryForm, ChampionshipForm, TeamForm, PlayerForm, PersonForm
from .filters import TeamFilter
from .fixture import generate_fixture, print_fixture
from django.http import HttpResponse
from django.contrib import messages
from itertools import zip_longest
from django.db.models import Q


################################--Inicio Person------------------------------------------
# --Crear Persona
def create_person(request):
    if request.method == "GET":
        form = PersonForm
        context = {"form": form}
        return render(request, "championship/person/create_person.html", context)
    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "persona creado correctamente!")
            return redirect("persons")
        else:
            messages.success(request, "Ingrese los datos correctamente")
            return render(
                request, "championship/person/create_person.html", {"form": form}
            )


# --Editar Persona------------------------------------------------------------------------
def edit_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES, instance=person)

        if form.is_valid():
            new_year_promotion = form.cleaned_data["year_promotion"]
            new_month_promotion = form.cleaned_data["month_promotion"]

            # Realiza la validación para verificar si la persona debe ser eliminada de algún equipo
            if person.team_set.exists():
                teams = person.team_set.all()
                for team in teams:
                    acceptable_range_start = team.year - (
                        team.year % 10
                    )  # Calcula el inicio del rango aceptable
                    acceptable_range_end = (
                        acceptable_range_start + 9
                    )  # Calcula el final del rango aceptable
                    # Procedemos con las validaciones
                    if (
                        person.is_jale == True
                        and acceptable_range_start
                        <= new_year_promotion
                        <= acceptable_range_end
                        and (
                            team.month == new_month_promotion
                            or team.month != new_month_promotion
                        )
                    ):
                        person.is_jale = True
                        person.save()
                    if (
                        person.is_jale == True
                        and not acceptable_range_start
                        <= new_year_promotion
                        <= acceptable_range_end
                    ):
                        person.is_jale = False
                        person.save()
                        team.Persons.remove(person)
                    if person.is_jale == False and team.year != new_year_promotion:
                        person.is_jale = False
                        person.save()
                        team.Persons.remove(person)
                    if person.is_jale == False and team.month != new_month_promotion:
                        person.is_jale = False
                        person.save()
                        team.Persons.remove(person)
            form.save()
            messages.success(request, "Persona editada correctamente!")
            return redirect("persons")
    else:
        form = PersonForm(instance=person)

    context = {"form": form}
    return render(request, "championship/person/edit_person.html", context)


# --Eliminar persona----------------------------------------------------------------------
def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("persons")


# --Ver persona----------------------------------------------------------------------
def view_person(request, person_id):
    person = Person.objects.get(id=person_id)
    context = {"person": person}
    return render(request, "championship/person/view_person.html", context)


# --Listar persona----------------------------------------------------------------------
def persons(request):
    persons = Person.objects.all()
    return render(request, "championship/person/persons.html", {"persons": persons})


################################--Fin persona-----------------------------------------------------


################################--Inicio Equipo --------------------------------------------------
# --Crear equipo----------------------------------------------------------------------
def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_month = form.cleaned_data["month"]
            team_year = form.cleaned_data["year"]
            team_group = form.cleaned_data["group"]
            if Team.objects.filter(
                month=team_month, year=team_year, group=team_group
            ).exists():
                form.add_error("group", "ya existe un equipo con dicho grupo")
            else:
                form.save()
                return redirect("teams")
    else:
        form = TeamForm()
    return render(request, "championship/Team/create_team.html", {"form": form})


# --Editar equipo----------------------------------------------------------------------
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    form = TeamForm(instance=team)
    players = team.Persons.all()

    if request.method == "POST":
        form = TeamForm(
            request.POST, instance=team
        )  # Pasa la instancia del equipo a editar
        if form.is_valid():
            team_month = form.cleaned_data["month"]
            team_year = int(form.cleaned_data["year"])
            team_group = form.cleaned_data["group"]

            if (
                Team.objects.filter(month=team_month, year=team_year, group=team_group)
                .exclude(pk=team_id)
                .exists()
            ):
                form.add_error("group", "Ya existe un equipo con dicho grupo")
            else:
                if team.championship_set.exists():
                    championships = team.championship_set.all()
                    for championship in championships:
                        cat = championship.categorys.name
                        acceptable_range_start = cat - (
                            cat % 10
                        )  # Calcula el inicio del rango aceptable
                        acceptable_range_end = (
                            acceptable_range_start + 9
                        )  # Calcula el final del rango aceptable
                        if acceptable_range_start <= team_year <= acceptable_range_end:
                            continue
                        championship.teams.remove(team)
                        team.Persons.clear()
                else:
                    team.Persons.clear()
        form.save()

        return redirect("teams")
    else:
        form = TeamForm(instance=team)  # Pasa la instancia del equipo a editar

    context = {"form": form, "teams": team}

    return render(request, "championship/team/edit_team.html", context)


# --Elminar equipo----------------------------------------------------------------------
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect("teams")


# --Lista equipos----------------------------------------------------------------------
def teams(request):
    teams = Team.objects.all()
    return render(request, "championship/team/teams.html", {"teams": teams})


# --Funcion de remover los personas  de un equipo ----------------------------------------
def remove_player_from_team(request, team_id, player_id):
    team = get_object_or_404(Team, pk=team_id)
    player = get_object_or_404(Person, pk=player_id)

    if request.method == "POST":
        # Elimina al jugador del equipo
        if player.is_jale == True:
            player.is_jale = False
            player.save()
            team.Persons.remove(player)
        else:
            team.Persons.remove(player)

    return redirect("view_team", team_id=team.id)


# --Esta funcion da detalles de un equipo-------------------------------------------------------
# --Esta funcion agrega las personas a un equipo
def view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = team.Persons.all()
    team_year = team.year
    year_range_start = team_year - (
        team_year % 10
    )  # Redondea hacia abajo al rango de 10 años más cercano
    year_range_end = year_range_start + 9

    players_available = Person.objects.filter(
        Q(year_promotion__isnull=True)
        | Q(year_promotion__gte=year_range_start, year_promotion__lte=year_range_end),
        team=None,
    )
    # Calcula cuántas personas cumplen la condición y cuántas no
    cumplen_condicion = 0
    no_cumplen_condicion = 0

    for player in players:
        if player.month_promotion == team.month and player.year_promotion == team.year:
            cumplen_condicion += 1
        else:
            no_cumplen_condicion += 1

    if request.method == "POST":
        player_id = request.POST.get("player_id")

        if player_id.isdigit():
            player = Person.objects.get(pk=player_id)
            # Verifica si se ha alcanzado el límite de 10 personas en el equipo
            if len(players) >= 10:
                messages.error(
                    request,
                    "El equipo ya tiene el máximo número de jugadores permitidos (10).",
                )
            else:
                # Verifica si el jugador cumple la condición
                if (
                    player.month_promotion == team.month
                    and player.year_promotion == team.year
                ):
                    cumplen_condicion += 1
                else:
                    no_cumplen_condicion += 1
                    player.is_jale = True
                    player.save()

                # Verifica si se han agregado 7 personas que cumplen la condición
                if no_cumplen_condicion <= 2:
                    team.Persons.add(player)
                    # Agrega un mensaje con la etiqueta "jugador_agregado"
                    messages.success(
                        request,
                        "Jugador agregado exitosamente.",
                        extra_tags="jugador_agregado",
                    )
                    return redirect("view_team", team_id=team.id)
                else:
                    messages.error(
                        request,
                        "No se pueden agregar más jugadores que no cumplen las condiciones",
                        extra_tags="no_cumple_condiciones",
                    )

        else:
            messages.warning(
                request, "ID de jugador no válido.", extra_tags="jugador_invalido"
            )
    no_cumple_condiciones_messages = [
        msg.message
        for msg in messages.get_messages(request)
        if msg.extra_tags == "no_cumple_condiciones"
    ]

    return render(
        request,
        "championship/team/view_team.html",
        {
            "team": team,
            "players": players,
            "players_available": players_available,
            "no_cumple_condiciones_messages": no_cumple_condiciones_messages,
        },
    )


################################--Fin Equipo-----------------------------------------------------------------


################################--Incio Campeonato----------------------------------------------------------------
# --Crear campeonato------------------------------------------------------------------------
def create_championship(request):
    if request.method == "POST":
        form = ChampionshipForm(request.POST)
        if form.is_valid():
            championship_category = form.cleaned_data["categorys"]
            print(championship_category)
            # Verifica si existe un campeaonato ya creado con la misma categoria y su su estado es true
            if Championship.objects.filter(
                categorys=championship_category, state=True
            ).exists():
                form.add_error(
                    "categorys",
                    "ya existe un campeonato con dicha categoria deshabilite dicho campeonato",
                )
            else:
                form.save()
                print("Formulario válido, redirigiendo...")
                return redirect("championships")
    else:
        form = ChampionshipForm()
    # Agrupa los campos en pares
    fields = form.visible_fields()
    grouped_fields = [fields[i : i + 2] for i in range(0, len(fields), 2)]

    return render(
        request,
        "championship/championship/create_championship.html",
        {"form": form, "grouped_fields": grouped_fields},
    )


# --Editar campeonato-------------------------------------------------------------------
def edit_championship(request, championship_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    cat = championship.categorys.name
    if request.method == "POST":
        form = ChampionshipForm(request.POST, instance=championship)
        if form.is_valid():
            cat1 = form.cleaned_data["categorys"]
            print(cat)
            print(cat1)
            if cat != cat1.name:
                print("amigo")
                championship.teams.clear()
                form.save()
            else:
                print("ssss")
                form.save()
            print("Formulario válido, redirigiendo...")
            return redirect("championships")
    else:
        form = ChampionshipForm(instance=championship)

    # Agrupa los campos en pares
    fields = form.visible_fields()
    grouped_fields = [fields[i : i + 2] for i in range(0, len(fields), 2)]

    context = {
        "form": form,
        "grouped_fields": grouped_fields,
        "championship": championship,  # Add the championship instance to the context
    }

    return render(request, "championship/championship/edit_championship.html", context)


# --Eliminar campeonato--------------------------------------------------------------------
def delete_championship(request, id):
    championship = get_object_or_404(Championship, pk=id)
    championship.delete()
    return redirect("championships")


# --Funcion remueve los equipos de un campeonato en especifico---------------------------
def remove_team_from_championship(request, championship_id, team_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    team = get_object_or_404(Team, pk=team_id)

    if request.method == "POST":
        # Elimina al equipo del campeonato
        championship.teams.remove(team)

    return redirect("add_team_championship", championship_id=championship.id)


# ..Listar campeonatos----------------------------------------------------------------------
def championships(request):
    championships = Championship.objects.all()
    context = {"championships": championships}
    return render(request, "championship/championship/championship.html", context)


# --Funcion que muestra los equipo que pertenecen a un equipo--------------------------------------
# --Funcion que agrega equipos a un campeonato
def add_team_championship(request, championship_id):
    championship = Championship.objects.get(pk=championship_id)
    teams = championship.teams.all()
    state_champioship = championship.state
    print(state_champioship)
    año_inicial = championship.categorys.name  # Reemplaza con el año inicial deseado
    año_final = año_inicial + 9  # Reemplaza con el año final deseado

    if championship.state:
        teams_availables = Team.objects.filter(
            year__gte=año_inicial, year__lte=año_final
        ).exclude(championship=championship)
    else:
        teams_availables = None

    if request.method == "POST":
        # Si el formulario se envió, procesa los datos aquí.
        teams_id = request.POST.get("championship_id")

        if teams_id.isdigit():
            team = Team.objects.get(pk=teams_id)
            championship.teams.add(team)
            # campeonato.save()
            return redirect("add_team_championship", championship_id=championship.id)
        else:
            messages.warning(
                request, "ID de equipo no válido.", extra_tags="equipo_invalido"
            )

    return render(
        request,
        "championship/championship/add_team_championship.html",
        {
            "championship": championship,
            "teams_available": teams_availables,
            "teams": teams,
        },
    )


################################--Fin Campeonato--------------------------------


################################--Incio Categoria--------------------------------
# --Crear categoria---------------------------------------------------------------
def create_category(request):
    if request.method == "GET":
        context = {"form": CategoryForm}
        return render(request, "championship/category/create_category.html", context)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categorys")


# --Lista categorias----------------------------------------------------------------
def categorys(request):
    categorys = Category.objects.all().order_by("name")
    context = {"categorys": categorys}
    return render(request, "championship/category/categorys.html", context)


# --Elimnat categoria---------------------------------------------------------------
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect("categorys")


# --Editar categoria----------------------------------------------------------------
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(
                "categorys"
            )  # Reemplaza 'list_categories' con la URL de la vista que muestra todas las categorías.
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "championship/category/edit_category.html",
        {"form": form, "category": category},
    )


####################################--Fin Categoria--------------------------------
# --Modulo Fixture----------------------------------------------------------------


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


"""
def add__player_team(request, player_id):
    team = Team.objects.get(pk=player_id)
    players_available = Person.objects.exclude(team=team)  # Obtener personas que no están en el equipo

    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Person.objects.get(pk=player_id)
        team.Persons.add(player)  # Agregar la persona al equipo
        
    return render(request, 'championship/team/add_player_team.html', {'team': team, 'players':players_available})
"""
"""
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
"""
"""
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
"""
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

"""
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

"""
revisar las urls
optimizar urls
falta editar, eliminar y validar
bloquear creacion de equipos cuando se genere el fixture
falta opcion de eliminar fixture
"""
