from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from django.contrib import messages
from championship.models import Anuncio, Championship, Category, Team, Game, ChampionshipTeam, Result, Person
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.utils.formats import date_format, time_format
from django.db.models import Sum

from .decorators import allowed_users

def home(request):
    anuncios = Anuncio.objects.all().order_by('-date', '-time')[:5]
    for anuncio in anuncios:
        # Formatear la fecha
        anuncio.date_formatted = date_format(anuncio.date, "j % F % Y") if anuncio.date else None

        # Formatear la hora
        anuncio.time_formatted = time_format(anuncio.time, "g:i A") if anuncio.time else None
    champ= ChampionshipTeam.objects.all().order_by('-id')
    print(champ)
    if(champ):
        for ch in champ:
            championship_id=ch.championship.id
            category_id=ch.category.id
            print(ch.category.id)
            print(ch.championship.id)
            print(ch)
        championship = get_object_or_404(Championship, pk=championship_id)
        category = get_object_or_404(Category, pk=category_id)
        # filtra los resultados del campeoanto en especifico
        results = Result.objects.filter(
            championship=championship_id, category=category_id).order_by('-pts')
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
        context = {'results': results,'result': result,
                'championships': championship, 'categorys': category, "anuncios": anuncios}
        return render(request, 'index.html', context)

    else:
        print("esta vacio")
        return render(request, 'index1.html')

    

def signin(request):  # login
    # retorna el valor del parametro next, si no 'None
    next_url = request.GET['next'] if request.GET.get(
        'next', None) != None else 'home'

    # si el usuario no esta autenticado
    if not request.user.is_authenticated:
        # manda a logearse
        if request.method == 'GET':
            return render(request, 'login.html', {'navoff': True})

        # recibe datos
        if request.method == 'POST':
            # valida usuario
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])

            # no existe el usuario
            if user is None:
                messages.success(request, "Usuario o contraseña incorrectos",extra_tags='deleted')
                return render(request, 'login.html')
            else:
                login(request, user)
                return redirect(next_url)
    else:
        return redirect(next_url)


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
@allowed_users(allowed_roles=['admin'])
def users(request):
    users = User.objects.all()
    context = {'users': users}

    return render(request, 'users/user/users.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def create_user(request):
    if request.method == 'GET':
        return render(request, 'users/user/create_user.html', {
            'form': UserForm
        })
    if request.method == 'POST':
        print(request.POST)

        if request.POST['password1'] == request.POST['password2']:

            try:
                form = UserForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(
                        username=request.POST['username'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                        password=request.POST['password1'])
                    group = Group.objects.get(id=request.POST['group'])
                    user.save()
                    user.groups.add(group)

                    messages.success(
                    request, "Usuario creado exitosamente.", extra_tags='created')
                    return redirect('users')

                else:
                    messages.success(
                        request, 'Ingrese los datos correctamente')
                    return render(request, 'users/user/create_user.html', {'form': form})

            except IntegrityError:
                messages.success(request, 'El usuario ya existe')
                return render(request, 'users/user/create_user.html', {'form': UserForm})

        messages.success(request, 'Contraseña incorrecta')
        return render(request, 'users/user/create_user.html', {'form': UserForm, })


@login_required
@allowed_users(allowed_roles=['admin'])
def edit_user(request, id):
    user = get_object_or_404(User, pk=id)

    if request.method == 'GET':
        form = UserForm()
        form.fields['username'].initial = user.username
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['email'].initial = user.email
        form.fields['group'].initial = user.groups.first()  #Suponiendo que un usuario sólo pueda estar en un grupo
        #Resto del código
        context = {'form': form}
        return render(request, 'users/user/edit_user.html', context)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        group = Group.objects.get(id=request.POST['group'])
        user.groups.clear()
        user.groups.add(group)

        user.save()
        messages.success(request, 'Usuario editado exitosamente.', extra_tags='created')
        return redirect('users')




@login_required
@allowed_users(allowed_roles=['admin'])
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    messages.success(
        request, f'El usuario ha sido eliminado exitosamente.', extra_tags='deleted')
    return redirect('users')

def denied(request):
    users = User.objects.all()
    context = {'users': users}

    return render(request, 'users/user/denied.html', context)