from django import forms
from .models import Category, Championship, Team, Player, Person
from .validators import validate_str
from django.core import validators
import datetime


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
        fields = ['name', 'year', 'discipline', 'categorys', 'state', 'rule']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del campeonato',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el año del campeonato',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'discipline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la disciplina del campeonato',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'categorys': forms.Select(attrs={
                'class': 'form-select',
                'required': False,
            }),
            'state': forms.CheckboxInput(attrs={
                'class': "form-check-input",
                'type': "checkbox",
                'style': 'margin-left: 15px;',
            }),
            'rule': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la regla del campeonato',
            'style': 'font-size: 20px; font-family: Montserrat;',
            'rows': 4,  # Establece la cantidad de filas del textarea según tus preferencias
            }),
        }
        labels = {
            'name': 'Nombre:',
            'year': 'Año:',
            'discipline': 'Disciplina:',
            'categorys': 'Categorias:',
            'state': 'Estado:',
            'rule': 'Reglas',
        }

MONTH_CHOICES = [
            ('Enero', 'Enero'),
            ('Febrero', 'Febrero'),
            ('Marzo', 'Marzo'),
            ('Abril', 'Abril'),
            ('Mayo', 'Mayo'),
            ('Junio', 'Junio'),
            ('Julio', 'Julio'),
            ('Agosto', 'Agosto'),
            ('Septiembre', 'Septiembre'),
            ('Octubre', 'Octubre'),
            ('Noviembre', 'Noviembre'),
            ('Diciembre', 'Diciembre'),
        ]

GROUP_CHOICES = [
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('E', 'E'),
        ]

current_year = datetime.date.today().year
YEAR_CHOICES = [(str(year), str(year)) for year in range(current_year, 1949, -1)]

class TeamForm(forms.ModelForm):
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Mes:'
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Año:'
    )
    group = forms.ChoiceField(
        choices=GROUP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Grupo:'
    )    
    state = forms.BooleanField(
        initial=True,  # Establece el valor predeterminado en True
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'margin-left: 15px;'}),
        label='Estado:'
    )

    class Meta:
        model = Team
        fields = ['month', 'year', 'group', 'state']


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
                  'promotion_sub_delegate', 'partner', 'month_promotion', 'year_promotion']
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
            'month_promotion': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'year_promotion': forms.TextInput(
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
            'month_promotion': 'Mes de promocion:',
            'year_promotion' : 'Año de promocion:',
        }
        