from django import forms
from .models import Category, Championship, Team, Person, Discipline, Season, PlayerGame, Game, Anuncio
from .validators import validate_str
from django.core import validators
import datetime
from django.forms import inlineformset_factory
#from django.forms.widgets import SelectDateWidget
#from django.forms.widgets import SelectTimeWidget
#from bootstrap_datepicker_plus import TimePickerInput

remainder = datetime.date.today().year % 10
current_year = datetime.date.today().year-remainder
CATEGORY_YEAR_CHOICES = [(str(year), str(year))
                         for year in range(current_year, 1949, -10)]


class CategoryForm(forms.ModelForm):
    name = forms.ChoiceField(
        choices=CATEGORY_YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3',
                            'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Año:'
    )

    class Meta:
        model = Category
        fields = ['name']


class DiciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de la disciplina',
                    'style': 'font-size: 20px; font-family: Montserrat;',
                }),
        }
        labels = {
            'name': 'Nombre',
        }


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de la disciplina',
                    'style': 'font-size: 20px; font-family: Montserrat;',
                }),
        }
        labels = {
            'name': 'Nombre',
        }


DISCIPLINA_CHOICES = [
    ('Futbol', 'Futbol'),
    ('Voley', 'Voley'),
    ('Basquet', 'Basquet'),
]


class ChampionshipForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = ['name', 'year', 'disciplines',
                  'seasons', 'categorys', 'state', 'rule']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del campeonato',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el año del campeonato',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'disciplines': forms.Select(attrs={
                'class': 'form-select',
                'required': False,
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'seasons': forms.Select(attrs={
                'class': 'form-select',
                'required': False,
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'categorys': forms.CheckboxSelectMultiple,
            'state': forms.Select(attrs={
                'class': 'form-select',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'rule': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese comentarios del campeonato',
                'style': 'font-size: 20px; font-family: Montserrat;',
                'rows': 4,
            }),
        }
        labels = {
            'name': 'Nombre:',
            'year': 'Año:',
            'disciplines': 'Disciplina',
            'seasons': 'Temporada:',
            'categorys': 'Categorias',
            'state': 'Habilitado:',
            'rule': 'Comentarios:',
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
CIVIL_STATUS_CHOICES = [
    ('Soltero', 'Soltero'),
    ('Casado', 'Casado'),
    ('Viudo', 'Viudo'),
    ('Divorciado', 'Divorciado'),
    ('Otro', 'Otro'),
]


current_year = datetime.date.today().year
YEAR_CHOICES = [(str(year), str(year))
                for year in range(current_year, 1949, -1)]


class TeamForm(forms.ModelForm):
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3',
                            'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Mes:'
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3',
                            'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Año:'
    )
    group = forms.ChoiceField(
        choices=GROUP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3',
                            'style': 'font-size: 20px; font-family: Montserrat;'}),
        label='Grupo:'
    )

    class Meta:
        model = Team
        fields = ['month', 'year', 'group', 'state']
        widgets = {
            'state': forms.Select(attrs={
                'class': 'form-select',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
        }
        labels = {
            'state': 'Habilitado:',
        }


class PersonBasicForm(forms.ModelForm):

    month_promotion = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Mes de promoción:'
    )
    year_promotion = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Año de promoción:'
    )

    class Meta:
        model = Person
        fields = ['name', 'surnames', 'dni', 'promotion_delegate',
                  'promotion_sub_delegate', 'partner', 'month_promotion', 'year_promotion']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control fa fa-home',

                }),
            'surnames': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'dni': forms.NumberInput(
                attrs={

                    'class': "form-control",
                }),
            'promotion_delegate': forms.Select(
                attrs={
                    'class': 'form-select',
                }),
            'partner': forms.Select(
                attrs={
                    'class': 'form-select',
                }),
            'promotion_sub_delegate': forms.Select(
                attrs={
                    'class': 'form-select',
                })
        }
        labels = {
            'name': 'Nombre:',
            'surnames': 'Apellidos:',
            'dni': 'Número de DNI:',
            'promotion_sub_delegate': 'Sub Delegado de promocion:',
            'promotion_delegate': 'Delegado de promocion:',
            'partner': 'Socio:'
        }


class PersonForm(forms.ModelForm):
    civil_status = forms.ChoiceField(
        choices=CIVIL_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Estado Civil:'
    )
    month_promotion = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Mes de promoción:'
    )
    year_promotion = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Año de promoción:'
    )

    class Meta:
        model = Person
        fields = ['name', 'surnames', 'birthdate', 'dni', 'military_card', 'province', 'department', 'address', 'district', 'activity',
                  'degree_instruction', 'civil_status', 'profession', 'phone', 'NSA_code', 'promotion_delegate',
                  'promotion_sub_delegate', 'partner', 'month_promotion', 'year_promotion', 'image']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control fa fa-home',

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
                    'class': "form-select",
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
            'NSA_code': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'type': 'file',
                }),
            'promotion_delegate': forms.Select(
                attrs={
                    'class': 'form-select',
                }),
            'partner': forms.Select(
                attrs={
                    'class': 'form-select',
                }),
            'promotion_sub_delegate': forms.Select(
                attrs={
                    'class': 'form-select',
                })
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
            'NSA_code': 'Código NSA:',
            'image': 'Imagen: ',
            'promotion_sub_delegate': 'Sub Delegado de promocion:',
            'promotion_delegate': 'Delegado de promocion:',
            'partner': 'Socio:'
        }


class PlayerGameForm(forms.ModelForm):
    class Meta:
        model = PlayerGame
        fields = ['card_yellow', 'card_red', 'goals']
        widgets = {
            'card_yellow': forms.NumberInput(
                attrs={
                    'class': "form-control form-control-sm",                    
                }),
            'card_red': forms.NumberInput(
                attrs={
                    'class': "form-control form-control-sm",
                }),
            'goals': forms.NumberInput(
                attrs={
                    'class': "form-control form-control-sm",
                }),
        }
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlayerGameForm, self).__init__(*args, **kwargs)

        if user and not user.is_authenticated:
            self.fields['card_yellow'].widget.attrs['disabled'] = True
            self.fields['card_red'].widget.attrs['disabled'] = True
            self.fields['goals'].widget.attrs['disabled'] = True

    

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['team1_goals', 'team2_goals']
        widgets = {
            'team1_goals': forms.NumberInput(
                attrs={
                    'class': "form-control border border-info-subtle ",
                    
                }),
            'team2_goals': forms.NumberInput(
                attrs={
                    'class': "form-control border border-info-subtle",
                }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(GameForm, self).__init__(*args, **kwargs)

        if user and not user.is_authenticated:
            self.fields['team1_goals'].widget.attrs['disabled'] = True
            self.fields['team2_goals'].widget.attrs['disabled'] = True



class AnuncioForm(forms.ModelForm):
    date = forms.DateField(
        label="Fecha",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", 'class': 'form-control', 'style': 'font-size: 20px; font-family: Montserrat;'}),
        input_formats=["%Y-%m-%d"]
    )
    time = forms.TimeField(
        label="Hora",
        required=False,
        widget=forms.TimeInput(
            attrs={"type": "time", 'class': 'form-control', 'placeholder': 'Seleccione la hora', 'style': 'font-size: 20px; font-family: Montserrat;'},
        ),
    )
    programar = forms.BooleanField(
        label="Programar",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    default = forms.BooleanField(
        label="Publicar ahora",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Anuncio
        fields = ['default', 'programar', 'date', 'time', 'championship', 'name', 'content', ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del anuncio',
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del anuncio',
                'style': 'font-size: 20px; font-family: Montserrat;',
                'rows': 4,
            }),
            'championship': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'style': 'font-size: 20px; font-family: Montserrat;',
            }),
        }
        labels = {
            'name': 'Título:',
            'content': 'Descripción:',
            'championship': 'Campeonato:',
            'date': 'Fecha:',
            'time': 'Hora:',
        }