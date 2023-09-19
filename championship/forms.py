from django import forms
from .models import Category, Championship, Team, Player


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
        }
        labels = {
            'name': 'Nombre',
        }


class ChampionshipForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = ['name', 'categorys', 'state']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'categorys': forms.Select(
                attrs={
                    'class': 'form-select',
                }),
            'state': forms.CheckboxInput(
                attrs={
                    'class': "form-check-input",
                    'type': "checkbox"
                }),
        }
        labels = {
            'name': 'Nombre',
            'categorys': 'Categorias',
            'state': 'Estado',
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'category', 'state']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'category': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'state': forms.CheckboxInput(
                attrs={
                    'class': "form-check-input",
                    'type': "checkbox"
                }),
        }
        labels = {
            'name': 'Nombre',
            'categorys': 'Categoria',
            'state': 'Estado',
        }


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'surnames']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'surnames': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),

        }
        labels = {
            'name': 'Nombre',
            'surnames': 'Apellidos',
        }
