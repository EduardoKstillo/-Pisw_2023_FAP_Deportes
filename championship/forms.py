from django import forms
from .models import Category, Championship, Team, Player, Person
from .validators import validate_str
from django.core import validators


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
                    'class': 'form-control','placeholder': 'Ingrese el nombre del campeonato', 'style': 'font-size: 20px; font-family: Montserrat;'
                }),
            'categories': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': False,
                }),
            'state': forms.CheckboxInput(
                attrs={
                    'class': "form-check-input",
                    'type': "checkbox", 'style': 'margin-left: 15px;'
                }),
        }
        labels = {
            'name': 'Nombre:',
            'categorys': 'Categorias:',
            'state': 'Estado:',
        }


class TeamForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del equipo', 'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Nombre:'
    )    

    state = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'margin-left: 15px;'}),
        label='Estado:'
    )

    class Meta:
        model = Team
        fields = ['name', 'state']


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

#---------------------------
class PersonForm(forms.ModelForm):
    
    class Meta:
        
        model = Person
        fields = ['name', 'surnames', 'birthdate', 'dni', 'military_card', 'province', 'department', 'address', 'district','activity',
                  'degree_instruction', 'civil_status', 'profession', 'phone', 'num_promotion', 'NSA_code', 'promotion_delegate',
                  'promotion_sub_delegate', 'partner']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'surnames': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'birthdate': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': "form-control",
                }),
            'dni': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
            'military_card': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
            'department': forms.Select(
                attrs={
                    'class': "form-control",
                }),
            'province': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'address': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'district': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'profession': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),

            'activity': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'degree_instruction': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'civil_status': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),

            'phone': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
            'num_promotion': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
            'promotion_delegate': forms.CheckboxInput(
                attrs={
                    'type': "checkbox",
                    'class': "form-check-input",
                }),
            'promotion_sub_delegate': forms.CheckboxInput(
                attrs={
                    'type': "checkbox",
                    'class': "form-check-input",
                }),
            'partner': forms.CheckboxInput(
                attrs={
                    'type': "checkbox",
                    'class': "form-check-input",
                }),
            'NSA_code': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
        }
        labels = {
            'name': 'Nombre:',
            'surnames': 'Apellidos:',
            'dni': 'Número de DNI:',
            'birthdate': 'Fecha de nacimiento:',
            'department': 'Departamento:',
            'military_card': 'N° de libreta militar:',
            'province': 'Provincia:',
            'profession': 'Profesión:',
            'activity': 'Actividad:',
            'degree_instruction': 'Grado de instrucción:',
            'civil_status': 'Estado civil:',
            'address': 'Dirección:',
            'district': 'Distrito:',
            'phone': 'N° de teléfono:',
            'num_promotion': 'N° de promoción:',
            'promotion_delegate': 'Delegado de promoción:',
            'promotion_sub_delegate': 'Sub-delegado de promoción:',
            'promotion_delegate': 'Socio:',
            'NSA_code': 'Código NSA:',
        }