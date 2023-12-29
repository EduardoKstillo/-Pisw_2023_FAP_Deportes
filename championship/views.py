from django.shortcuts import render, redirect, get_object_or_404
from .models import (Category, Championship, Team, Game,
                     Person, ChampionshipTeam, Discipline, Season, PlayerGame, Result)
from .forms import (CategoryForm, ChampionshipForm, TeamForm,
                    PersonBasicForm, PersonForm, DiciplineForm, SeasonForm, PlayerGameForm)
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


# --Inicio Person------------------------------------------
@login_required
def create_person(request):
    if request.method == "GET":
        form = PersonBasicForm
        context = {"form": form}
        return render(request, "championship/person/create_person.html", context)
    if request.method == "POST":
        form = PersonBasicForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "persona creado correctamente!")
            return redirect("persons")
        else:
            messages.success(request, "Ingrese los datos correctamente")
            return render(
                request, "championship/person/create_person.html", {
                    "form": form}
            )


@login_required
def edit_person(request, person_id):
    
    person = get_object_or_404(Person, pk=person_id)

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
                        person.promotion_delegate = False
                        person.save()
                        # remuevo a la persona de ese equipo
                        team.persons.remove(person)

            form.save()
            messages.success(request, "¡Persona editada correctamente!")
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
def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return redirect("persons")


@login_required
def view_person(request, person_id):
    person = Person.objects.get(id=person_id)
    context = {"person": person}
    return render(request, "championship/person/view_person.html", context)


@login_required
def persons(request):
    persons = Person.objects.all()
    myfilter = PersonFilter(request.GET, queryset=persons)
    persons = myfilter.qs
    context = {"persons": persons, "filter": myfilter}
    return render(request, "championship/person/persons.html", context)


# --Fin persona-----------------------------------------------------


# --Inicio Equipo --------------------------------------------------
@login_required
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
                messages.success(request, "¡Equipo creado correctamente!", extra_tags='created')
                return redirect("teams")
    else:
        form = TeamForm()

    return render(request, "championship/team/create_team.html", {"form": form})


# --Editar equipo----------------------------------------------------------------------
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
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
                        if player.promotion_delegate :
                            player.promotion_delegate = False
                            player.save()

                # Guardar el formulario después de realizar todas las verificaciones
                form.save()
                return redirect("teams")
    else:
        form = TeamForm(instance=team)
        player_associated =team.persons.all()
        championship_team = ChampionshipTeam.objects.filter(team = team)

    context = {"form": form, "teams": team, "player_associated" : player_associated, "championship_team": championship_team }
    return render(request, "championship/team/edit_team.html", context)
   



# --Elminar equipo----------------------------------------------------------------------
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_year = team.year
    team_mouth = team.month
    team_group = team.group
    players = Person.objects.filter(team=team)
    for player in players:
        player.promotion_delegate = False
        player.save()
    team.delete()

    messages.success(request, f'El equipo "{team_mouth}.{team_year}.{team_group}" ha sido eliminado exitosamente.', extra_tags='deleted')
    return redirect("teams")



# --Lista equipos------------------------------------------------------------------------
def teams(request):
    teams = Team.objects.all()
    return render(request, "championship/team/teams.html", {"teams": teams})


# --Funcion de remover los personas  de un equipo ----------------------------------------
def remove_player_from_team(request, team_id, player_id):
    team = get_object_or_404(Team, pk=team_id)
    player = get_object_or_404(Person, pk=player_id)
    player_name = player.name

    next = request.POST.get("next", "/")

    if request.method == "POST":
        # Elimina al jugador del equipo
        if player.is_jale == True or player.promotion_delegate== True:
            player.is_jale = False
            player.promotion_delegate = False
            player.save()
            team.persons.remove(player)
        else:
            team.persons.remove(player)

    messages.success(
        request, f'El jugador "{player_name}" ha sido removido del equipo exitosamente.')
    return redirect(next)


# --Funcion para zar una persona si es delegado de equipo
def actualizar_jugador(request, player_id):
    if request.method == "POST":
        try:
            jugador = Person.objects.get(pk=player_id)
            # Realizar la lógica para zar el campo promotion_delegate a True
            jugador.promotion_delegate = True
            jugador.save()
            return JsonResponse({"message": "Jugador zado correctamente"})
        except Person.DoesNotExist:
            return JsonResponse({"error": "Jugador no encontrado"}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# --Funcion para zar una persona en caso ya no sea delegado de equipo
def actualizar_jugador1(request, player_id):
    print("amigo")
    if request.method == "POST":
        try:
            jugador = Person.objects.get(pk=player_id)
            # Realizar la lógica para zar el campo promotion_delegate a True
            jugador.promotion_delegate = False
            jugador.save()
            return JsonResponse({"message": "Jugador zado correctamente"})
        except Person.DoesNotExist:
            return JsonResponse({"error": "Jugador no encontrado"}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# --Esta funcion da detalles de un equipo-------------------------------------------------------
# --Esta funcion agrega las personas a un equipo


def view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = team.persons.all()
    team_year = team.year
    year_range_start = team_year - (
        team_year % 10
    )  # Redondea hacia abajo al rango de 10 años más cercano
    year_range_end = year_range_start + 9
    if team.state == True :
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



# --Fin Equipo-----------------------------------------------------------------


# --Incio Campeonato----------------------------------------------------------------
# --Crear campeonato------------------------------------------------------------------------
def create_championship(request):
    if request.method == "POST":
        form = ChampionshipForm(request.POST)
        if form.is_valid():
            form.save()
            print("Formulario válido, redirigiendo...")
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


def edit_championship(request, championship_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    
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
                for old_category in deleted_categories :
                    ChampionshipTeam.objects.filter(championship=championship, category=old_category).delete()

            # Puedes redirigir a donde corresponda después de editar
            return redirect("championships")
    else:
        form = ChampionshipForm(instance=championship)
        TeamChapionshipCategory = ChampionshipTeam.objects.filter(championship=championship)
        categoryall = Category.objects.all()

    fields = form.visible_fields()
    grouped_fields = [fields[i: i + 3] for i in range(0, len(fields), 3)]
    context = {"form": form, "championships": championship, "grouped_fields": grouped_fields, "TeamChapionshipCategory" : TeamChapionshipCategory ,"categoryall": categoryall}

    return render(
        request,
        "championship/championship/edit_championship.html",
        context,
    )



    return render(
        request,
        "championship/championship/edit_championship.html",
        context,
    )


# --Eliminar campeonato--------------------------------------------------------------------


def delete_championship(request, id):
    championship = get_object_or_404(Championship, pk=id)
    championship_name = championship.name
    championship_year = championship.year
    championship_season = championship.seasons
    championship.delete()

    messages.success(
        request, f'El campeonato "{championship_name}/{championship_year}/{championship_season}" ha sido eliminado exitosamente.')
    return redirect("championships")


# --Funcion remueve los equipos de un campeonato en especifico---------------------------
def remove_team_from_championship(request, championship_id, category_id, team_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)
    team = get_object_or_404(Team, pk=team_id)
    team_month = team.month
    team_year = team.year
    team_group = team.group

    if request.method == "POST":
        # Elimina al equipo del campeonato
        championship_team = ChampionshipTeam.objects.get(
            championship=championship, category=category, team=team
        )
        championship_team.delete()

    messages.success(
        request, f'El equipo "{team_month}.{team_year}.{team_group}" ah sido removido de la categoria exitosamente.')
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
                request, "ID de equipo no válido.", extra_tags="equipo_invalido"
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
                messages.success(request, "¡Categoría creada correctamente!", extra_tags='created')
                return redirect("categorys")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            context = {"form": form}
            return render(request, "championship/category/create_category.html", context)


# --Lista categorias----------------------------------------------------------------
def categorys(request):
    categorys = Category.objects.all().order_by("name")
    context = {"categorys": categorys}
    return render(request, "championship/category/categorys.html", context)


# --Elimnat categoria---------------------------------------------------------------
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, f'La categoría "{category.name}" ha sido eliminada exitosamente.', extra_tags='deleted')
    return redirect("categorys")


# --Editar categoria----------------------------------------------------------------
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
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

                    messages.success(request, "¡Categoría editada correctamente!", extra_tags='edited')
                    return redirect("categorys")
            else:
                messages.success(request, "No se realizaron cambios", extra_tags='deleted')                
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
def disciplines(request):
    disciplines = Discipline.objects.all().order_by("name")
    context = {"disciplines": disciplines}
    return render(request, "championship/discipline/disciplines.html", context)


# --Crear disciplinas---------------------------------------------------------------
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
                messages.success(request, "Disciplina creada exitosamente.",extra_tags='created')
                return redirect("disciplines")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            messages.error(request, "Solo se aceptan letras")
            context = {"form": form}
            return render(request, "championship/discipline/create_discipline.html", context)


# --Elimnar disciplinas---------------------------------------------------------------
def delete_discipline(request, discipline_id):
    discipline = get_object_or_404(Discipline, pk=discipline_id)
    discipline_name = discipline.name
    discipline.delete()

    messages.success(
        request, f'La disciplina "{discipline_name}" ha sido eliminada exitosamente.', extra_tags='deleted')
    return redirect("disciplines")


# --Editar disciplinas----------------------------------------------------------------
def edit_discipline(request, discipline_id):
    discipline = get_object_or_404(Discipline, id=discipline_id)
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
                        request, "Disciplina editada correctamente",extra_tags='edited')
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


def seasons(request):
    seasons = Season.objects.all().order_by("name")
    context = {"seasons": seasons}
    return render(request, "championship/season/seasons.html", context)


# --Crear temporadas---------------------------------------------------------------


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
                messages.success(request, "Temporada creada exitosamente.")
                return redirect("seasons")
        else:
            # Si el formulario no es válido, vuelve a mostrar el formulario con los errores.
            messages.error(request, "Solo se aceptan letras")
            context = {"form": form}
            return render(request, "championship/season/create_season.html", context)


# --Elimnar temporadas---------------------------------------------------------------


def delete_season(request, season_id):
    season = get_object_or_404(Season, pk=season_id)
    season_name = season.name
    season.delete()

    messages.success(
        request, f'La temporada "{season_name}" ha sido eliminada exitosamente.')
    return redirect("seasons")


# --Editar temporadas----------------------------------------------------------------
def edit_season(request, season_id):
    season = get_object_or_404(Season, id=season_id)
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
                        request, "Temporada editado correctamente")
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
    print(championship_teams)
    # obtengo una lista de los ID de los equipos
    team_ids = championship_teams.values_list("team_id")
    # filtro los equipos con tales IDs
    teams = Team.objects.filter(id__in=team_ids)
    print(teams)

    # Verificar si ya existe un fixture para el campeonato
    existing_fixture = Game.objects.filter(
        championship=championship, category=category)
    if existing_fixture.exists():
        championship = get_object_or_404(Championship, pk=championship_id)
        category = get_object_or_404(Category, pk=category_id)
        print("fixture existente")
        print(existing_fixture)
        grouped_fixtures = {}
        for fixture in existing_fixture:
            round_number = fixture.round_number
            if round_number not in grouped_fixtures:
                grouped_fixtures[round_number] = []
            grouped_fixtures[round_number].append(fixture)

        # messages.success(request, "El fixture ya esta creado!")
        # retorna el fixture existente del campeanato
        print(grouped_fixtures)

        context = {'grouped_fixtures': grouped_fixtures,
                   'championships': championship, 'categorys': category}
        return render(request, "championship/game/fixture.html", context)

    # crear el fixture, los diferentes juegos que tendra el campeonato
    fixture = generate_fixture(teams, championship, category)
    print("nuevo fixture")
    print(fixture)

    # filtra todos los juegos creados anteriormente
    fixture = Game.objects.filter(championship=championship, category=category)
    grouped_fixtures = {}

    for fixture in fixture:
        round_number = fixture.round_number
        if round_number not in grouped_fixtures:
            grouped_fixtures[round_number] = []
        grouped_fixtures[round_number].append(fixture)

    print("groupfixtures")

    print(grouped_fixtures)

    context = {'grouped_fixtures': grouped_fixtures,
               'championships': championship, 'categorys': category}
    messages.success(request, "Fixture creado exitosamente.",extra_tags='created')

    return render(request, "championship/game/fixture.html", context)


def game(request, game_id):
    # obtengo el game en especifico
    game = get_object_or_404(Game, id=game_id)
    # Obtener jugadores de cada equipo
    players_team1 = game.team1.persons.all()
    players_team2 = game.team2.persons.all()
    print("equipo 1", game.team1.persons.all())
    print(game.team2.persons.all())

    # Crear formularios para cada jugador
    forms_team1 = [PlayerGameForm(prefix=f'equipo1-{jugador.id}', initial={
                                  'player': jugador, 'game': game}) for jugador in players_team1]
    forms_team2 = [PlayerGameForm(prefix=f'equipo2-{jugador.id}', initial={
                                  'player': jugador, 'game': game}) for jugador in players_team2]
    print("equipo 1", forms_team1)

    if request.method == 'POST':
        # goles de cada equipo
        team1_goals = request.POST['team1_goals']
        team2_goals = request.POST['team2_goals']
        # valida si los goles son numeros
        if team1_goals.isdigit() and team1_goals.isdigit():
            # instancio valores de cada jugador
            forms_team1 = [PlayerGameForm(request.POST, prefix=f'equipo1-{jugador.id}', initial={
                                          'player': jugador, 'game': game}) for jugador in players_team1]
            forms_team2 = [PlayerGameForm(request.POST, prefix=f'equipo2-{jugador.id}', initial={
                                          'player': jugador, 'game': game}) for jugador in players_team2]
            # verifico la valides del los formularios
            if all(form.is_valid() for form in forms_team1 + forms_team2):
                for form in forms_team1 + forms_team2:
                    # inserto goles para cada equipo
                    game.team1_goals = team1_goals
                    game.team2_goals = team2_goals
                    # cambia el estado del juego a finalizado
                    # game.status = False
                    form.save()
                    game.save()
                #
                table_result_championship(game)
                # redirige al fixture
                return redirect('create_fixture', championship_id=game.championship.id, category_id=game.category.id)

        else:
            # messages.success(request, "Ingrese valores validos")
            print('algo salio mal')

    return render(request, "championship/game/game.html", {'game': game, 'forms_team1': forms_team1, 'forms_team2': forms_team2})


# instancia la tabla de posiciones
def table_result_championship(game):
    # Actualizar los resultados del equipo1
    result_team1, created = Result.objects.get_or_create(
        team=game.team1, championship=game.championship, category=game.category)
    result_team1.pj += 1
    result_team1.pg += 1 if game.team1_goals > game.team2_goals else 0
    result_team1.pe += 1 if game.team1_goals == game.team2_goals else 0
    result_team1.pp += 1 if game.team1_goals < game.team2_goals else 0
    result_team1.gf += int(game.team1_goals)
    result_team1.gc += int(game.team2_goals)
    result_team1.dg = result_team1.gf - result_team1.gc
    result_team1.pts = 3 * result_team1.pg + result_team1.pe
    result_team1.save()

    # Actualizar los resultados del equipo2
    result_team2, created = Result.objects.get_or_create(
        team=game.team2, championship=game.championship, category=game.category)
    result_team2.pj += 1
    result_team2.pg += 1 if game.team2_goals > game.team1_goals else 0
    result_team2.pe += 1 if game.team2_goals == game.team1_goals else 0
    result_team2.pp += 1 if game.team2_goals < game.team1_goals else 0
    result_team2.gf += int(game.team2_goals)
    result_team2.gc += int(game.team1_goals)
    result_team2.dg = result_team2.gf - result_team2.gc
    result_team2.pts = 3 * result_team2.pg + result_team2.pe
    result_team2.save()


# --Listar tabla de posiciones----------------------------------------------------------------------
def tabla_posiciones(request, championship_id, category_id):
    championship = get_object_or_404(Championship, pk=championship_id)
    category = get_object_or_404(Category, pk=category_id)
    # filtra los resultados del campeoanto en especifico
    results = Result.objects.filter(
        championship=championship_id, category=category_id).order_by('-pts')

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
    #players_game = PlayerGame.objects.filter(game__in=leaked_games)
    players_game = Person.objects.filter(playergame__game__in=leaked_games).distinct()

    result = (
    players_game
    .annotate(total_goals=Sum('playergame__goals'))
    .values('name', 'team__month', 'total_goals')
    .order_by('-total_goals')
    )

    context = {'result':result, 'championships': championship, 'categorys': category}
    
    return render(request, 'championship/fixture/goleadores.html', context)

"""
def add__player_team(request, player_id):
    team = Team.objects.get(pk=player_id)
    players_available = Person.objects.exclude(team=team)  # Obtener personas que no están en el equipo

    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Person.objects.get(pk=player_id)
        team.persons.add(player)  # Agregar la persona al equipo
        
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
