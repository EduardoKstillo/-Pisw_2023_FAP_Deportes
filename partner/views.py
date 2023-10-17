from django.shortcuts import render, redirect, get_object_or_404
from .models import Partner
from .forms import PartnerForm, UserForm
from .filters import PartnerFilter

from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .decorators import allowed_users


def home(request):
    return render(request, 'index.html')


def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'login.html', {'navoff': True})

        if request.method == 'POST':
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'login.html', {
                    'message': 'user or password incorrect',
                    'navoff': True
                })
            else:
                login(request, user)
                return redirect('partner')
    else:
        return redirect('partner')


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


@login_required
@allowed_users(allowed_roles=['admin'])
def partner(request):
    partners = Partner.objects.all()
    myfilter = PartnerFilter(request.GET, queryset=partners)
    partners = myfilter.qs
    context = {'partners': partners, 'filter': myfilter}

    return render(request, 'users/partner/partner.html', context)


@login_required
def create_partner(request):
    if request.method == 'GET':
        form = PartnerForm
        context = {'form': form}
        return render(request, 'users/partner/create_partner.html', context)
    if request.method == 'POST':
        form = PartnerForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Socio creado correctamente!')
            return redirect('partner')
        else:
            messages.success(request, 'Ingrese los datos correctamente')
            return render(request, 'users/partner/create_partner.html', {'form': form})
        # return redirect('home')


@login_required
@allowed_users(allowed_roles=['admin'])
def detail_partner(request, id):
    partner = get_object_or_404(Partner, pk=id)

    if request.method == 'GET':
        form = PartnerForm(instance=partner)
        context = {'form': form, 'partner': partner}
        return render(request, 'users/partner/detail_partner.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def edit_partner(request, id):
    partner = get_object_or_404(Partner, pk=id)

    if request.method == 'GET':
        form = PartnerForm(instance=partner)
        context = {'form': form, 'partner': partner}
        return render(request, 'users/partner/edit_partner.html', context)

    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Socio editado correctamente!')
            return redirect('partner')
        else:
            messages.success(request, 'Ingrese los datos correctamente')
            return render(request, 'users/partner/create_partner.html', {'form': form})


@login_required
@allowed_users(allowed_roles=['admin'])
def delete_partner(request, id):
    partner = get_object_or_404(Partner, pk=id)
    partner.delete()
    return redirect('partner')


@login_required
@allowed_users(allowed_roles=['admin'])
def details_partner(request, id):
    partner = get_object_or_404(Partner, pk=id)

    if request.method == 'GET':
        form = PartnerForm(instance=partner)
        context = {'form': form}
        return render(request, 'users/partner/details_partner.html', context)
