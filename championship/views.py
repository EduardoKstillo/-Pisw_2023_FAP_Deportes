from django.shortcuts import render, redirect, get_object_or_404
from .models import (Category, Championship, Team, Game,
                     Person, ChampionshipTeam, Discipline, Season, PlayerGame, Result, Anuncio)
from .forms import (CategoryForm, ChampionshipForm, TeamForm,
                    PersonBasicForm, PersonForm, DiciplineForm, SeasonForm, PlayerGameForm, GameForm, AnuncioForm)
from django.forms import inlineformset_factory

from django.contrib.auth.decorators import login_required
from .filters import PersonFilter, TeamFilter
from .fixture import generate_fixture
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from copy import deepcopy
from django.db import transaction
from django.db.models import Sum
import locale
from django.utils import timezone
from django.utils.formats import date_format, time_format
from partner.decorators import allowed_users


# --Inicio Person------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def create_person(request):
    if request.method == "GET":
        form = PersonBasicForm
        context = {"form": form}
        return render(request, "championship/person/create_person.html", context)
    if request.method == "POST":
        form = PersonBasicForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "persona creado correctamente!", extra_tags='created')
            return redirect("persons")
        else:
            messages.success(request, "Ingrese los datos correctamente")
            return render(
                request, "championship/person/create_person.html", {
                    "form": form}
            )


@login_required
@allowed_users(allowed_roles=['admin'])
def edit_person(request, person_id):

    person = get_object_or_404(Person, pk=person_id)

    # Verificar si la persona está asociada a algún juego en un campeonato con fixture ya creado
    associated_games = PlayerGame.objects.filter(player=person)
    has_fixture = any(game.game.championship.state and Game.objects.filter(championship=game.game.championship).exists() for game in associated_games)

    if has_fixture:
        messages.warning(request, "No se puede modificar la persona porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("persons")

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES, instance=person)

        if form.is_valid():
            # Acceder a los datos limpios y validados
            new_year_promotion = int(form.cleaned_data["year_promotion"])
            # new_month_promotion = form.cleaned_data["month_promotion"]
            # si la persona exisiste en un equipo
            if person.team_set.exists():
                teams = person.team_set.all()
                for team in teams:
                    # Calcula el inicio del rango aceptable
                    acceptable_range_start = team.year - (team.year % 10)
                    # Calcula el final del rango aceptable
                    acceptable_range_end = (acceptable_range_start + 9)

                    # si la año de la persona no esta dentro del rango permitido
                    if not (acceptable_range_start <= new_year_promotion <= acceptable_range_end):
                        person.team_delegate = False
                        person.save()
                        # remuevo a la persona de ese equipo
                        team.persons.remove(person)

            form.save()
            messages.success(request, "¡Persona editada correctamente!", extra_tags='created')
            return redirect("persons")
        else:
            messages.success(request, "Ingrese los datos correctamente")

    else:
        form = PersonForm(instance=person)

    # si no tiene equipo
    context = {"form": form}

    # si la persona tiene equipo
    if person.team_set.exists():
        team = person.team_set.first()
        context = {"form": form, "team": team}

    return render(request, "championship/person/edit_person.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    # Verificar si la persona está asignada a algún equipo en una categoría con fixture ya creado
    associated_teams = Team.objects.filter(persons=person)
    has_fixture = any(
        ChampionshipTeam.objects.filter(
            team=team,
            championship__state=True,
            category__game__isnull=False
        ).exists() for team in associated_teams
    )

    if has_fixture:
        messages.warning(
            request, "No se puede eliminar la persona porque está asignada a un equipo que pertenece a una categoría participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("persons")

    person.delete()
    messages.success(
        request, f'La persona ha sido eliminada exitosamente.', extra_tags='created')
    return redirect("persons")


@login_required
@allowed_users(allowed_roles=['admin'])
def view_person(request, person_id):
    person = Person.objects.get(id=person_id)
    context = {"person": person}
    return render(request, "championship/person/view_person.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def persons(request):
    persons = Person.objects.all()
    myfilter = PersonFilter(request.GET, queryset=persons)
    persons = myfilter.qs
    context = {"persons": persons, "filter": myfilter}
    return render(request, "championship/person/persons.html", context)


# --Fin persona-----------------------------------------------------


# --Inicio Equipo --------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_month = form.cleaned_data["month"]
            team_year = form.cleaned_data["year"]
            team_group = form.cleaned_data["group"]

            if Team.objects.filter(month=team_month, year=team_year, group=team_group).exists():
                form.add_error("group", "ya existe un equipo con dicho grupo")
            else:
                form.save()
                messages.success(
                    request, "¡Equipo creado correctamente!", extra_tags='created')
                return redirect("teams")
    else:
        form = TeamForm()

    return render(request, "championship/team/create_team.html", {"form": form})


# --Editar equipo----------------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # Verificar si el equipo está asociado a algún campeonato con fixture ya creado
    associated_championships = ChampionshipTeam.objects.filter(team=team)
    has_fixture = any(championship.championship.state and Game.objects.filter(championship=championship.championship).exists() for championship in associated_championships)

    if has_fixture:
        messages.warning(request, "No se puede modificar el equipo porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("teams")
    form = TeamForm(instance=team)
    players = team.persons.all()

    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)

        if form.is_valid():
            # Extraer los datos del formulario
            team_month = form.cleaned_data["month"]
            team_year = int(form.cleaned_data["year"])
            team_group = form.cleaned_data["group"]

            # Verificar si existe un equipo con los nuevos valores
            if Team.objects.filter(month=team_month, year=team_year, group=team_group).exclude(pk=team_id).exists():
                form.add_error("group", "Ya existe un equipo con dicho grupo")
            else:
                # Verificar si el equipo está asociado a algún campeonato
                championship_teams = ChampionshipTeam.objects.filter(team=team)
                for championship_team in championship_teams:
                    category_start = int(championship_team.category.name)
                    category_end = category_start + 9
                    if not (category_start <= team_year <= category_end):
                        print("Eliminando campeonato asociado")
                        championship_team.delete()

                # Eliminar jugadores que no cumplen con los requisitos
                # Calcula el inicio del rango aceptable
                acceptable_range_start = team.year - (team.year % 10)
                # Calcula el final del rango aceptable
                acceptable_range_end = (acceptable_range_start + 9)
                for player in players:
                    if not (acceptable_range_start <= player.year_promotion <= acceptable_range_end):
                        print("Eliminando jugador no apto")
                        team.persons.remove(player)
                        if player.team_delegate:
                            player.team_delegate = False
                            player.save()

                # Guardar el formulario después de realizar todas las verificaciones
                form.save()
                messages.success(
                    request, f'El equipo ha sido editado correctamente.', extra_tags='created')
                return redirect("teams")
    else:
        form = TeamForm(instance=team)
        player_associated = team.persons.all()
        championship_team = ChampionshipTeam.objects.filter(team=team)

    context = {"form": form, "teams": team, "player_associated": player_associated,
               "championship_team": championship_team}
    return render(request, "championship/team/edit_team.html", context)


# --Eliminar equipo----------------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    # Verificar si el equipo está asociado a alguna categoría que pertenezca a algún campeonato con fixture ya creado
    associated_categories = Category.objects.filter(
        Q(championshipteam__team=team) & Q(championshipteam__championship__state=True)
    )

    if associated_categories.exists():
        messages.warning(
            request, "No se puede eliminar el equipo porque pertenece a una categoría que está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("teams")

    team_year = team.year
    team_month = team.month
    team_group = team.group
    players = Person.objects.filter(team=team)
    
    for player in players:
        player.team_delegate = False
        player.save()

    team.delete()

    messages.success(
        request, f'El equipo "{team_month}.{team_year}.{team_group}" ha sido eliminado exitosamente.', extra_tags='deleted')
    return redirect("teams")


# --Lista equipos------------------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def teams(request):
    teams = Team.objects.all()
    return render(request, "championship/team/teams.html", {"teams": teams})


# --Funcion de remover los personas  de un equipo ----------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def remove_player_from_team(request, team_id, player_id):
    team = get_object_or_404(Team, pk=team_id)

    # Verificar si el equipo está asociado a algún campeonato con fixture ya creado
    associated_championships = ChampionshipTeam.objects.filter(team=team)
    has_fixture = any(championship.championship.state and Game.objects.filter(championship=championship.championship).exists() for championship in associated_championships)

    if has_fixture:
        messages.warning(request, "No se puede eliminar jugadores del equipo porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("teams")
    
    player = get_object_or_404(Person, pk=player_id)
    player_name = player.name

    next = request.POST.get("next", "/")

    if request.method == "POST":
        # Elimina al jugador del equipo
        if player.is_jale == True or player.team_delegate == True:
            player.is_jale = False
            player.team_delegate = False
            player.save()
            team.persons.remove(player)
        else:
            team.persons.remove(player)

    messages.success(
        request, f'El jugador "{player_name}" ha sido removido del equipo exitosamente.', extra_tags='deleted')
    return redirect(next)


# --Funcion para zar una persona si es delegado de equipo
@login_required
@allowed_users(allowed_roles=['admin'])
def actualizar_jugador(request, player_id):
    if request.method == "POST":
        try:
            jugador = Person.objects.get(pk=player_id)
            # Realizar la lógica para zar el campo team_delegate a True
            jugador.team_delegate = True
            jugador.save()
            return JsonResponse({"message": "Jugador zado correctamente"})
        except Person.DoesNotExist:
            return JsonResponse({"error": "Jugador no encontrado"}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# --Funcion para zar una persona en caso ya no sea delegado de equipo
@login_required
@allowed_users(allowed_roles=['admin'])
def actualizar_jugador1(request, player_id):
    print("amigo")
    if request.method == "POST":
        try:
            jugador = Person.objects.get(pk=player_id)
            # Realizar la lógica para zar el campo team_delegate a True
            jugador.team_delegate = False
            jugador.save()
            return JsonResponse({"message": "Jugador zado correctamente"})
        except Person.DoesNotExist:
            return JsonResponse({"error": "Jugador no encontrado"}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# --Esta funcion da detalles de un equipo-------------------------------------------------------
# --Esta funcion agrega las personas a un equipo

@login_required
@allowed_users(allowed_roles=['admin'])
def view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Verificar si el equipo está asociado a algún campeonato con fixture ya creado
    associated_championships = ChampionshipTeam.objects.filter(team=team)
    has_fixture = any(championship.championship.state and Game.objects.filter(championship=championship.championship).exists() for championship in associated_championships)

    players = team.persons.all()
    team_year = team.year
    year_range_start = team_year - (team_year % 10)
    year_range_end = year_range_start + 9

    if has_fixture:
        messages.warning(request, "No se puede agregar jugadores al equipo porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        players_available = None
    else:
        if team.state:
            players_available = Person.objects.filter(
                Q(year_promotion__isnull=True)
                | Q(year_promotion__gte=year_range_start, year_promotion__lte=year_range_end),
                team=None,
            )
        else:
            players_available = None
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
            if len(players) >= 25:
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
                if no_cumplen_condicion <= 25:
                    team.persons.add(player)
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
                request, "ID de jugador no válido.", extra_tags="deleted"
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


# --Fin Equipo-----------------------------------------------------------------


# --Incio Campeonato----------------------------------------------------------------
# --Crear campeonato------------------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def create_championship(request):
    if request.method == "POST":
        form = ChampionshipForm(request.POST)
        if form.is_valid():
            form.save()
            print("Formulario válido, redirigiendo...")
            messages.success(
                request, "¡Campeonato creado correctamente!", extra_tags='created')
            return redirect("championships")
    else:
        form = ChampionshipForm()

    fields = form.visible_fields()
    grouped_fields = [
        fields[i: i + 3] for i in range(0, len(fields), 3)
    ]  # Cambio en el paso

    return render(
        request,
        "championship/championship/create_championship.html",
        {"form": form, "grouped_fields": grouped_fields},
    )


# --Editar campeonato-------------------------------------------------------------------

@login_required
@allowed_users(allowed_roles=['admin'])
def edit_championship(request, championship_id):
    championship = get_object_or_404(Championship, pk=championship_id)

    # Verificar si ya existe un fixture para el campeonato y la categoría en cuestión
    existing_fixture = Game.objects.filter(championship=championship)

    if existing_fixture.exists():
        messages.warning(request, "No se puede remover el equipo porque ya existe un fixture para el campeonato y la categoría.", extra_tags='deleted')
        return redirect("championships")

    if request.method == "POST":
        form = ChampionshipForm(request.POST, instance=championship)
        if form.is_valid():
            # Guarda las categorías antes de guardar el formulario
            categories_before_save = set(championship.categorys.all())
            # Guarda el campeonato actualizado
            form.save()
            # Obtiene las categorías después de guardar el formulario
            categories_after_save = set(form.cleaned_data['categorys'])
            # Calcula las categorías eliminadas
            deleted_categories = categories_before_save - categories_after_save
            # Imprime los nombres de las categorías eliminadas
            for deleted_category in deleted_categories:
                print(f"Categoría eliminada: {deleted_category.name}")
            # verfica con las categorías eliminas o desmarcadas y procede con elminar los jugadores del tal categoria campeonato
            with transaction.atomic():
                for old_category in deleted_categories:
                    ChampionshipTeam.objects.filter(
                        championship=championship, category=old_category).delete()

            # Puedes redirigir a donde corresponda después de editar
            return redirect("championships")
    else:
        form = ChampionshipForm(instance=championship)
        TeamChapionshipCategory = ChampionshipTeam.objects.filter(
            championship=championship)
        categoryall = Category.objects.all()

    fields = form.visible_fields()
    grouped_fields = [fields[i: i + 3] for i in range(0, len(fields), 3)]
    context = {"form": form, "championships": championship, "grouped_fields": grouped_fields,
               "TeamChapionshipCategory": TeamChapionshipCategory, "categoryall": categoryall}

    return render(
        request,
        "championship/championship/edit_championship.html",
        context,
    )


# --Eliminar campeonato--------------------------------------------------------------------

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_championship(request, id):
    championship = get_object_or_404(Championship, pk=id)
    championship_name = championship.name
    championship_year = championship.year
    championship_season = championship.seasons
    championship.delete()

    messages.success(
        request, f'El campeonato "{championship_name}/{championship_year}/{championship_season}" ha sido eliminado exitosamente.', extra_tags='deleted')
    return redirect("championships")


# --Funcion remueve los equipos de un campeonato en especifico---------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def remove_team_from_championship(request, championship_id, category_id, team_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)
    team = get_object_or_404(Team, pk=team_id)

    # Verificar si ya existe un fixture para el campeonato y la categoría en cuestión
    existing_fixture = Game.objects.filter(championship=championship, category=category)

    if existing_fixture.exists():
        messages.warning(request, "No se puede remover el equipo porque ya existe un fixture para el campeonato y la categoría.", extra_tags='deleted')
        return redirect("add_team_championship", championship_id=championship.id, categorys_id=category.id)

    if request.method == "POST":
        # Elimina al equipo del campeonato
        championship_team = ChampionshipTeam.objects.get(
            championship=championship, category=category, team=team
        )
        championship_team.delete()

    messages.success(
        request, f'El equipo "{team.month}.{team.year}.{team.group}" ha sido removido de la categoría exitosamente.')
    return redirect("add_team_championship", championship_id=championship.id, categorys_id=category.id)

# --Listar campeonatos----------------------------------------------------------------------


def championships(request):

    championships = Championship.objects.all()
    context = {"championships": championships}
    return render(request, "championship/championship/championship.html", context)


# --Funcion que muestra los equipo que pertenecen a un equipo--------------------------------------
# --Funcion que agrega equipos a un campeonato

def add_team_championship(request, championship_id, categorys_id):

    championship = Championship.objects.get(pk=championship_id)
    category = Category.objects.get(pk=categorys_id)

    # Verificar si ya existe un fixture para el campeonato y la categoría en cuestión
    existing_fixture = Game.objects.filter(championship=championship, category=category)

    # teams=Team.objects.all()
    championship_teams = ChampionshipTeam.objects.filter(
        championship_id=championship_id, category_id=categorys_id
    )
    team_ids = championship_teams.values_list("team_id")
    teams = Team.objects.filter(id__in=team_ids)
    # teams = Team.objects.filter(championship=championship, category=category)
    state_champioship = championship.state
    print(state_champioship)
    año_inicial = category.name  # Reemplaza con el año inicial deseado
    año_final = año_inicial + 9  # Reemplaza con el año final deseado

    if existing_fixture.exists():
        messages.warning(request, "No se pueden añadir equipos porque ya existe un fixture para el campeonato y la categoría.", extra_tags='deleted')
        teams_availables = None # Cambia "teams" por la URL a la que deseas redirigir
    else:
        if championship.state:
            teams_availables = Team.objects.filter(
                year__gte=año_inicial, year__lte=año_final, state=True
            ).exclude(id__in=team_ids)
        else:
            teams_availables = None

        if request.method == "POST":
            # Si el formulario se envió, procesa los datos aquí.
            teams_id = request.POST.get("championship_id")

            if teams_id.isdigit():
                team = Team.objects.get(pk=teams_id)
                championship_category_team = ChampionshipTeam(
                    championship=championship, category=category, team=team
                )
                championship_category_team.save()

                # campeonato.save()
                return redirect(
                    "add_team_championship",
                    championship_id=championship.id,
                    categorys_id=category.id,
                )
            else:
                messages.warning(
                    request, "ID de equipo no válido.", extra_tags="deleted"
                )

    return render(
        request,
        "championship/championship/add_team_championship.html",
        {
            "championship": championship,
            "teams_available": teams_availables,
            "teams": teams,
            "category": category,
        },
    )


# --Ver campeonato y sus categorias pertenecientes----------------------------------------------------------------------

def view_championship(request, championship_id):
    championship = Championship.objects.get(pk=championship_id)
    categorys = championship.categorys.all()

    return render(
        request,
        "championship/championship/championship_category.html",
        {"championship": championship, "categorys": categorys},
    )


# --Fin Campeonato--------------------------------


# --Incio Categoria--------------------------------
# --Crear categoria---------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def create_category(request):
    if request.method == "GET":
        context = {"form": CategoryForm}
        return render(request, "championship/category/create_category.html", context)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if Category.objects.filter(name=category_name).exists():
                # Si ya existe una categoria con el mismo nombre, muestra un mensaje de error o toma la acción que consideres apropiada.
                context = {"form": form}
                messages.success(request, "Ya existe tal categoria")
                return render(request, "championship/category/create_category.html", context)
            else:
                form.save()
                messages.success(
                    request, "¡Categoría creada correctamente!", extra_tags='created')
                return redirect("categorys")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            context = {"form": form}
            return render(request, "championship/category/create_category.html", context)


# --Lista categorias----------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def categorys(request):
    categorys = Category.objects.all().order_by("name")
    context = {"categorys": categorys}
    return render(request, "championship/category/categorys.html", context)


# --Elimnat categoria---------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    # Verificar si la categoría está asociada a algún campeonato con fixture ya creado
    associated_championships = ChampionshipTeam.objects.filter(category=category)
    has_fixture = any(Game.objects.filter(championship=championship.championship).exists() for championship in associated_championships)

    if has_fixture:
        messages.warning(request, "No se puede eliminar la categoría porque está asignada a un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("categorys")

    category.delete()

    messages.success(
        request, f'La categoría "{category.name}" ha sido eliminada exitosamente.', extra_tags='deleted')
    return redirect("categorys")


# --Editar categoria----------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Verificar si la categoría está asociada a algún campeonato con fixture ya creado
    associated_championships = Championship.objects.filter(categorys=category)
    has_fixture = any(championship.state and Game.objects.filter(championship=championship).exists() for championship in associated_championships)

    if has_fixture:
        messages.warning(request, "No se puede modificar la categoría porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("categorys")

    name_category = int(category.name)
    form = CategoryForm(instance=category)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            category_name = int(form.cleaned_data['name'])
            if name_category != category_name:
                if Category.objects.filter(name=category_name).exists():
                    # Si ya existe una categoria con el mismo nombre, muestra un mensaje de error o toma la acción que consideres apropiada.
                    context = {"form": form}
                    messages.success(request, "Ya existe tal categoria")
                    return render(request, "championship/category/edit_category.html", context)
                else:
                    form.save()
                    associated_championship = Championship.objects.filter(
                        Q(categorys=category) & Q(state=True))
                    # Itera sobre los campeonatos y obtén los equipos asociados
                    # for championship in associated_championship:
                    # championship_teams = ChampionshipTeam.objects.filter(championship=championship, category=category)
                    # Itera sobre los ChampionshipTeam y obtén los equipos
                    # for championship_team in championship_teams:

                    # team = championship_team.team
                    # print(team.month)

                    for champioship in associated_championship:
                        ChampionshipTeam.objects.filter(
                            championship=champioship, category=category).delete()

                    messages.success(
                        request, "¡Categoría editada correctamente!", extra_tags='edited')
                    return redirect("categorys")
            else:
                messages.success(
                    request, "No se realizaron cambios", extra_tags='deleted')
                return redirect("categorys")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            associated_championship = Championship.objects.filter(
                Q(categorys=category) & Q(state=True))
            context = {"form": form,
                       "associated_championship": associated_championship}
            return render(request, "championship/category/edit_category.html", context)
    else:
        associated_championship = Championship.objects.filter(
            Q(categorys=category) & Q(state=True))
        championship_teams = ChampionshipTeam.objects.filter(category=category)

    context = {"form": form, "category": category, "associated_championship":
               associated_championship, "championship_teams": championship_teams}
    return render(request, "championship/category/edit_category.html", context)


# --Fin Categoria--------------------------------

# --Inicio Disciplinas--------------------------------
# ----Listar disciplinas
@login_required
@allowed_users(allowed_roles=['admin'])
def disciplines(request):
    disciplines = Discipline.objects.all().order_by("name")
    context = {"disciplines": disciplines}
    return render(request, "championship/discipline/disciplines.html", context)


# --Crear disciplinas---------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def create_discipline(request):
    if request.method == "GET":
        context = {"form": DiciplineForm}
        return render(
            request, "championship/discipline/create_discipline.html", context
        )

    if request.method == "POST":
        form = DiciplineForm(request.POST)
        if form.is_valid():
            discipline_name = form.cleaned_data['name']
            normalized_name = discipline_name.lower()  # Normaliza a minúsculas
            # Usamos name__iexact para comparar sin tomar en cuenta mayusculas o minisculas
            if Discipline.objects.filter(name__iexact=normalized_name).exists():
                # Si ya existe una disciplina con el mismo nombre (ignorando mayúsculas/minúsculas), muestra un mensaje de error.
                context = {"form": form}
                messages.error(
                    request, "Ya existe una disciplina con ese nombre.")
                return render(request, "championship/discipline/create_discipline.html", context)
            else:
                form.save()
                messages.success(
                    request, "Disciplina creada exitosamente.", extra_tags='created')
                return redirect("disciplines")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            messages.error(request, "Solo se aceptan letras")
            context = {"form": form}
            return render(request, "championship/discipline/create_discipline.html", context)


# --Elimnar disciplinas---------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def delete_discipline(request, discipline_id):
    discipline = get_object_or_404(Discipline, pk=discipline_id)
    discipline_name = discipline.name
    # Verificar si la disciplina está asociada a algún campeonato
    associated_championships = Championship.objects.filter(disciplines=discipline)

    if associated_championships.exists():
        # Si la disciplina está asociada a algún campeonato, mostrar un mensaje de error
        messages.error(
            request, f'La disciplina "{discipline_name}" está asociada a campeonatos y no puede ser eliminada.', extra_tags='deleted')
    else:
        # Si no está asociada a ningún campeonato, eliminar la disciplina
        discipline.delete()
        messages.success(
            request, f'La disciplina "{discipline_name}" ha sido eliminada exitosamente.', extra_tags='deleted')

    return redirect("disciplines")


# --Editar disciplinas----------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def edit_discipline(request, discipline_id):
    discipline = get_object_or_404(Discipline, id=discipline_id)

    # Verificar si la disciplina está asociada a algún campeonato con fixture ya creado
    associated_championships = Championship.objects.filter(disciplines=discipline)
    has_fixture = any(championship.state and Game.objects.filter(championship=championship).exists() for championship in associated_championships)

    if has_fixture:
        messages.warning(request, "No se puede modificar la disciplina porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("disciplines")

    form = DiciplineForm(instance=discipline)

    if request.method == "POST":
        form = DiciplineForm(request.POST, instance=discipline)
        if form.is_valid():
            discipline_name = form.cleaned_data['name']
            normalized_name = discipline_name.lower()  # Normaliza a minúsculas

            if form.has_changed():  # Verifica si ha habido cambios en el formulario
                if Discipline.objects.filter(name__iexact=discipline_name).exists():
                    # Si ya existe una disciplina con el mismo nombre, muestra un mensaje de error o toma la acción que consideres apropiada.
                    context = {"form": form}
                    messages.error(request, "Ya existe tal disciplina")
                    return render(request, "championship/discipline/edit_discipline.html", context)
                else:
                    form.save()
                    messages.success(
                        request, "Disciplina editada correctamente", extra_tags='edited')
                    return redirect("disciplines")
            else:
                messages.info(
                    request, "No se realizaron cambios en la disciplina.")
            return redirect("disciplines")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            messages.error(request, "Solo se aceptan letras")
            associated_championship = Championship.objects.filter(
                Q(disciplines=discipline) & Q(state=True))
            context = {"form": form,
                       "associated_championship": associated_championship}
            return render(request, "championship/discipline/edit_discipline.html", context)
    else:
        associated_championship = Championship.objects.filter(
            Q(disciplines=discipline) & Q(state=True))

    context = {"form": form, "disciplines": discipline,
               "associated_championship": associated_championship}
    return render(request, "championship/discipline/edit_discipline.html", context)


# --Fin Disciplina--------------------------------
# --Inicio Temporada--------------------------------
# ----Listar temporadas--------------------------------

@login_required
@allowed_users(allowed_roles=['admin'])
def seasons(request):
    seasons = Season.objects.all().order_by("name")
    context = {"seasons": seasons}
    return render(request, "championship/season/seasons.html", context)


# --Crear temporadas---------------------------------------------------------------

@login_required
@allowed_users(allowed_roles=['admin'])
def create_season(request):
    if request.method == "GET":
        context = {"form": SeasonForm}
        return render(request, "championship/season/create_season.html", context)

    if request.method == "POST":
        form = SeasonForm(request.POST)
        if form.is_valid():
            season_name = form.cleaned_data['name']
            normalized_name = season_name.lower()  # Normaliza a minúsculas
            # Usamos name__iexact para comparar sin tomar en cuenta mayusculas o minisculas
            if Season.objects.filter(name__iexact=season_name).exists():
                # Si ya existe una disciplina con el mismo nombre (ignorando mayúsculas/minúsculas), muestra un mensaje de error.
                context = {"form": form}
                messages.error(request, "Ya existe tal temporada")
                return render(request, "championship/season/create_season.html", context)
            else:
                form.save()
                messages.success(request, "Temporada creada exitosamente.", extra_tags='created')
                return redirect("seasons")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            messages.error(request, "Solo se aceptan letras")
            context = {"form": form}
            return render(request, "championship/season/create_season.html", context)


# --Elimnar temporadas---------------------------------------------------------------

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_season(request, season_id):
    season = get_object_or_404(Season, pk=season_id)
    season_name = season.name
    # Verificar si la temporada está asociada a algún campeonato
    associated_championships = Championship.objects.filter(seasons=season)

    if associated_championships.exists():
        # Si la temporada está asociada a algún campeonato, mostrar un mensaje de error
        messages.error(
            request, f'La temporada "{season_name}" está asociada a campeonatos y no puede ser eliminada.', extra_tags='deleted')
    else:
        # Si no está asociada a ningún campeonato, eliminar la temporada
        season.delete()
        messages.success(
            request, f'La temporada "{season_name}" ha sido eliminada exitosamente.', extra_tags='deleted')

    return redirect("seasons")


# --Editar temporadas----------------------------------------------------------------
@login_required
@allowed_users(allowed_roles=['admin'])
def edit_season(request, season_id):
    season = get_object_or_404(Season, id=season_id)

    # Verificar si la temporada está asociada a algún campeonato con fixture ya creado
    associated_championships = Championship.objects.filter(seasons=season)
    has_fixture = any(championship.state and Game.objects.filter(championship=championship).exists() for championship in associated_championships)

    if has_fixture:
        messages.warning(request, "No se puede modificar la temporada porque está participando en un campeonato con fixture ya creado.", extra_tags='deleted')
        return redirect("seasons")

    form = SeasonForm(instance=season)
    # form = deepcopy(original_form)

    if request.method == "POST":
        form = SeasonForm(request.POST, instance=season)
        if form.is_valid():
            season_name = form.cleaned_data['name']
            normalized_name = season_name.lower()  # Normaliza a minúsculas

            if form.has_changed():  # Verifica si ha habido cambios en el formulario
                if Season.objects.filter(name__iexact=season_name).exists():
                    # Si ya existe una disciplina con el mismo nombre, muestra un mensaje de error o toma la acción que consideres apropiada.
                    context = {"form": form}
                    messages.error(request, "Ya existe tal temporada")
                    return render(request, "championship/season/edit_season.html", context)
                else:
                    form.save()
                    messages.success(
                        request, "Temporada editado correctamente", extra_tags='created')
                    return redirect("seasons")
            else:
                messages.info(
                    request, "No se realizaron cambios en la temporada.")
                return redirect("seasons")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            messages.error(request, "Solo se aceptan letras")
            associated_championship = Championship.objects.filter(
                Q(seasons=season) & Q(state=True))
            # form = deepcopy(original_form)
            context = {"form": form,
                       "associated_championship": associated_championship}
            return render(request, "championship/season/edit_season.html", context)
    else:
        # Obtiene los campeonatos asociados a tal categoria
        associated_championship = Championship.objects.filter(
            Q(seasons=season) & Q(state=True))

    context = {"form": form, "seasons": season,
               "associated_championship": associated_championship}
    return render(request, "championship/season/edit_season.html", context)


# --Fin temporadas--------------------------------


# --Modulo Fixture----------------------------------------------------------------
def create_fixture(request, championship_id, category_id):
    # obtengo el campeonato y la categoria en especifico
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)

    # equipos del campeonato por categoria
    championship_teams = ChampionshipTeam.objects.filter(
        championship_id=championship_id, category_id=category_id
    )
    # obtengo una lista de los ID de los equipos
    team_ids = championship_teams.values_list("team_id")
    # filtro los equipos con tales IDs
    teams = Team.objects.filter(id__in=team_ids)

    # Verificar si ya existe un fixture para el campeonato
    existing_fixture = Game.objects.filter(
        championship=championship, category=category)
    if existing_fixture.exists():
        championship = get_object_or_404(Championship, pk=championship_id)
        category = get_object_or_404(Category, pk=category_id)
        grouped_fixtures = {}
        for fixture in existing_fixture:
            round_number = fixture.round_number
            if round_number not in grouped_fixtures:
                grouped_fixtures[round_number] = []
            grouped_fixtures[round_number].append(fixture)

        # messages.success(request, "El fixture ya esta creado!")
        # retorna el fixture existente del campeanato

        context = {'grouped_fixtures': grouped_fixtures,
                   'championships': championship, 'categorys': category}
        return render(request, "championship/game/fixture.html", context)

    # crear el fixture, los diferentes juegos que tendra el campeonato
    fixture = generate_fixture(teams, championship, category)

    # filtra todos los juegos creados anteriormente
    fixture = Game.objects.filter(championship=championship, category=category)
    grouped_fixtures = {}
    if fixture.count() == 0:
        context = {'championships': championship, 'categorys': category}
        print("entro aqui")
        messages.success(request, "No se puede crear un fixture sin equipos.",
                         extra_tags='deleted')
        return render(request, "championship/game/fixture.html", context)

    for fixture in fixture:
        round_number = fixture.round_number
        if round_number not in grouped_fixtures:
            grouped_fixtures[round_number] = []
        grouped_fixtures[round_number].append(fixture)

    context = {'grouped_fixtures': grouped_fixtures,
               'championships': championship, 'categorys': category}
    messages.success(request, "Fixture creado exitosamente.",
                     extra_tags='created')

    return render(request, "championship/game/fixture.html", context)


@allowed_users(allowed_roles=['admin','arbitro'])
def game_status(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    if request.method == 'POST':
        # recupera el body que mande con fech
        # data = json.loads(request.body)
        # recuepera el atributo status que esta dentro del body
        # status = data.get('status')
        game.state = not game.state
        print(game.state)
        game.save()

        return JsonResponse({'estado': game.state})


def game(request, game_id):
    # obtengo el game en especifico
    game = get_object_or_404(Game, id=game_id)

    # si alguno de los equipos es DESCANSA, entonces no puedes ingresar al form (te redirecciona)
    if game.state or (game.team1.name or game.team2.name) == 'DESCANSA':
        return redirect('create_fixture', championship_id=game.championship.id, category_id=game.category.id)

    # instacion el Gamefor con game
    game_form = GameForm(user=request.user, instance=game)

    # Obtener jugadores de cada equipo
    players_team1 = game.team1.persons.all()
    players_team2 = game.team2.persons.all()

    forms_team1 = []
    for jugador in players_team1:
        try:
            player_game_instance = jugador.playergame_set.get(game=game)
        except PlayerGame.DoesNotExist:
            # Si el PlayerGame no existe, créalo antes de intentar obtenerlo
            player_game_instance = PlayerGame(player=jugador, game=game)
            player_game_instance.save()

        forms_team1.append(PlayerGameForm(user=request.user,
            prefix=f'equipo1-{jugador.id}', instance=player_game_instance))

    forms_team2 = []
    for jugador in players_team2:
        try:
            player_game_instance = jugador.playergame_set.get(game=game)
        except PlayerGame.DoesNotExist:
            # Si el PlayerGame no existe, créalo antes de intentar obtenerlo
            player_game_instance = PlayerGame(player=jugador, game=game)
            player_game_instance.save()

        forms_team2.append(PlayerGameForm(user=request.user,
            prefix=f'equipo2-{jugador.id}', instance=player_game_instance))

    if request.method == 'POST':
        game_form = GameForm(request.POST, instance=game)

        forms_team1 = [PlayerGameForm(request.POST, prefix=f'equipo1-{jugador.id}', instance=jugador.playergame_set.get(
            game=game) if jugador.playergame_set.filter(game=game).exists() else None) for jugador in players_team1]

        forms_team2 = [PlayerGameForm(request.POST, prefix=f'equipo2-{jugador.id}', instance=jugador.playergame_set.get(
            game=game) if jugador.playergame_set.filter(game=game).exists() else None) for jugador in players_team2]

        if game_form.is_valid() and all(form.is_valid() for form in forms_team1 + forms_team2):

            # Validar la suma de goles para el equipo 1
            total_goles_equipo1 = sum(form.cleaned_data.get(
                'goals', 0) for form in forms_team1)
            if total_goles_equipo1 != game_form.cleaned_data.get('team1_goals'):
                messages.error(
                    request, f"La suma de goles de los jugadores del equipo {game.team1.month}.{game.team1.year}.{game.team1.group} no coincide con los goles totales del equipo.")
                return render(request, "championship/game/game.html", {'game': game, 'game_form': game_form, 'forms_team1': forms_team1, 'forms_team2': forms_team2})

            # Validar la suma de goles para el equipo 2
            total_goles_equipo2 = sum(form.cleaned_data.get(
                'goals', 0) for form in forms_team2)
            if total_goles_equipo2 != game_form.cleaned_data.get('team2_goals'):
                messages.error(
                    request, f"La suma de goles de los jugadores del equipo {game.team2.month}.{game.team2.year}.{game.team2.group} no coincide con los goles totales del equipo.")
                return render(request, "championship/game/game.html", {'game': game, 'game_form': game_form, 'forms_team1': forms_team1, 'forms_team2': forms_team2})

            for form in forms_team1 + forms_team2:
                form.save()

            game_form.save()

            table_result_championship(game)
            return redirect('create_fixture', championship_id=game.championship.id, category_id=game.category.id)
        else:
            messages.error(
                request, "Número de goles o tarjetas invalidas")

    return render(request, "championship/game/game.html", {'game': game, 'game_form': game_form, 'forms_team1': forms_team1, 'forms_team2': forms_team2})

# instancia la tabla de posiciones


def table_result_championship(game):
    # Actualizar los resultados del equipo1

    result_team1, created = Result.objects.get_or_create(round_number = game.round_number,
        team=game.team1, championship=game.championship, category=game.category)
    
    result_team1.pj = 1
    result_team1.pg = 1 if game.team1_goals > game.team2_goals else 0
    result_team1.pe = 1 if game.team1_goals == game.team2_goals else 0
    result_team1.pp = 1 if game.team1_goals < game.team2_goals else 0
    result_team1.gf = int(game.team1_goals)
    result_team1.gc = int(game.team2_goals)
    result_team1.dg = result_team1.gf - result_team1.gc
    result_team1.pts = 3 * result_team1.pg + result_team1.pe
    result_team1.save()

    # Actualizar los resultados del equipo2
    result_team2, created = Result.objects.get_or_create(round_number = game.round_number,
        team=game.team2, championship=game.championship, category=game.category)
    result_team2.pj = 1
    result_team2.pg = 1 if game.team2_goals > game.team1_goals else 0
    result_team2.pe = 1 if game.team2_goals == game.team1_goals else 0
    result_team2.pp = 1 if game.team2_goals < game.team1_goals else 0
    result_team2.gf = int(game.team2_goals)
    result_team2.gc = int(game.team1_goals)
    result_team2.dg = result_team2.gf - result_team2.gc
    result_team2.pts = 3 * result_team2.pg + result_team2.pe
    result_team2.save()

    # game state change to finished
    game.state = True
    game.save()


    #game.sum_team_points = result_team1.pts + result_team2.pts
    #game.save()


# --Listar tabla de posiciones----------------------------------------------------------------------
def tabla_posiciones(request, championship_id, category_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)

    leaked_games = Result.objects.filter(
        category_id=category_id, championship_id=championship_id)
    
    # Sumar las columnas pj, pg, etc, agrupadas por equipo
    results = leaked_games.values('team_id').annotate(
        pj=Sum('pj'),
        pg=Sum('pg'),
        pe=Sum('pe'),
        pp=Sum('pp'),
        gf=Sum('gf'),
        gc=Sum('gc'),
        dg=Sum('dg'),
        pts=Sum('pts'),
    ).values(
        'team__month',
        'team__year', 
        'team__group',
        'pj',
        'pg',
        'pe',
        'pp',
        'gf',
        'gc',
        'dg',
        'pts').order_by('-pts')
    

    context = {'results': results,
               'championships': championship, 'categorys': category}

    return render(request, 'championship/fixture/tabla_posiciones.html', context)


def amonestaciones(request, championship_id, category_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)
    # Filtrar los juegos según category_id y championship_id
    leaked_games = Game.objects.filter(
        category_id=category_id, championship_id=championship_id)

    # Filtrar PlayerGame (jugadores por partido o Game)
    players_game = PlayerGame.objects.filter(game__in=leaked_games)

    # Obtener jugadores implicados
    # jugadores_implicados = Person.objects.filter(playergame__game__in=leaked_games).distinct()

    # Sumar las columnas card_red, card_yellow, y goals agrupadas por jugador
    players_summary = players_game.values('player').annotate(
        total_card_red=Sum('card_red'),
        total_card_yellow=Sum('card_yellow'),
    )

    # Obtener información de los jugadores
    players = Person.objects.all()

    context = {
        'players_summary': players_summary,
        'players': players,
        'championships': championship,
        'categorys': category
    }

    return render(request, 'championship/fixture/amonestaciones.html', context)


def goleadores(request, championship_id, category_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)
    # Filtrar los juegos según category_id y championship_id
    leaked_games = Game.objects.filter(
        category_id=category_id, championship_id=championship_id)

    # Filtrar PlayerGame (jugadores por partido o Game)
    # players_game = PlayerGame.objects.filter(game__in=leaked_games)
    players_game = Person.objects.filter(
        playergame__game__in=leaked_games).distinct()

    result = (
        players_game
        .annotate(total_goals=Sum('playergame__goals'))
        .values('name', 'team__month', 'team__year', 'team__group', 'total_goals')
        .order_by('-total_goals')
    )

    context = {'result': result,
               'championships': championship, 'categorys': category}

    return render(request, 'championship/fixture/goleadores.html', context)


# ------------------------------------------ Modulo Anuncios
# --Crear anuncio
@login_required
@allowed_users(allowed_roles=['admin'])
def create_anuncio(request):
    if request.method == "POST":
        form = AnuncioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "¡Anuncio creado correctamente!", extra_tags='created')
            return redirect("anuncios")
    else:
        form = AnuncioForm()

    return render(request, "championship/anuncio/create_anuncio.html", {"form": form})

#--Editar anuncio
#--Listar anucio
@login_required
@allowed_users(allowed_roles=['admin'])
def anuncios(request):
    anuncios = Anuncio.objects.all().order_by('-date', '-time')

    # Configura la localización en español para la fecha
    # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Formatea las fechas y horas en español
    for anuncio in anuncios:
        # Formatear la fecha
        anuncio.date_formatted = date_format(anuncio.date, "j % F % Y") if anuncio.date else None

        # Formatear la hora
        anuncio.time_formatted = time_format(anuncio.time, "g:i A") if anuncio.time else None

    return render(request, "championship/anuncio/anuncios.html", {"anuncios": anuncios})

# --Editar anuncio
@login_required
@allowed_users(allowed_roles=['admin'])
def edit_anuncio(request, anuncio_id):
    # Obtener la instancia del Anuncio desde la base de datos
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)

    if request.method == 'POST':
        # Rellenar el formulario con los datos actuales del Anuncio
        form = AnuncioForm(request.POST, instance=anuncio)
        if form.is_valid():
            # Guardar los datos del formulario si son válidos
            form.save()
            messages.success(
                request, "¡Anuncio editado correctamente!", extra_tags='created')
            # Redireccionar a algún lugar, por ejemplo, a la página de detalle del anuncio
            return redirect('anuncios')
    else:
        # Si el método no es POST, mostrar el formulario con los datos actuales del Anuncio
        form = AnuncioForm(instance=anuncio)

    return render(request, "championship/anuncio/edit_anuncio.html", {'form': form})

# --Eliminar anuncio
@login_required
@allowed_users(allowed_roles=['admin'])
def delete_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    anuncio_name = anuncio.name
    anuncio.delete()
    messages.success(
        request, f'El anuncio "{anuncio_name}" ha sido eliminado exitosamente.', extra_tags='deleted')        
    return redirect("anuncios")

def denied(request):
    
    return render(request, "championship/anuncio/denied.html")