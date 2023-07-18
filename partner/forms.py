from django import forms
from django.contrib.auth.models import User
from .models import Partner


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'groups', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }),
            'groups': forms.Select(
                attrs={
                    'class': "form-select",
                }),
            'password': forms.PasswordInput(
                attrs={
                    'class': "form-control",
                }),
        }
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'groups': 'Rol',
            'password': 'Contraseña',
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'
        """
        fields = ['name', 'surnames', 'dni']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'surnames': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'dni': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
        }
        labels = {
            'name': 'Nombre',
            'surnames': 'Apellidos',
            'dni': 'Dni',
        }
        """
