from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from django.contrib import messages

from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .decorators import allowed_users


def home(request):
    return render(request, 'index.html')


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
                return render(request, 'login.html', {
                    'message': 'user or password incorrect',
                    'navoff': True
                })
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
                        request, 'Usuario creado correctamente!')
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
        form = UserForm(instance=user)
        context = {'form': form}
        return render(request, 'users/user/edit_user.html', context)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        group = Group.objects.get(id=request.POST['groups'])
        user.groups.clear()
        user.groups.add(group)

        user.save()
        return redirect('users')


@login_required
@allowed_users(allowed_roles=['admin'])
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('users')
