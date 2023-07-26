from django import forms
from django.contrib.auth.models import Group
from .models import Partner
from .validators import validate_str
from django.core import validators


class UserForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(label='Nombres', validators=[validate_str], max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(label='Apellidos', validators=[validate_str], max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Correo electronico', required=True, validators=[validators.EmailValidator(message="Invalid Email")], max_length=200, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    group = forms.ModelChoiceField(label='Rol', queryset=Group.objects.all(), required=True,  widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


"""

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].validators.append(validate_amazing)

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

"""


class PartnerForm(forms.ModelForm):
    
    class Meta:
        
        model = Partner
        fields = ['name', 'surnames', 'birthdate', 'num_carnet', 'dni', 'military_card', 'province', 'department', 'address', 'district',
                  'activity',
                  'degree_instruction', 'civil_status', 'dni', 'profession', 'phone', 'num_promotion', 'NSA_code', 'promotion_delegate']
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
            'num_carnet': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
            'military_card': forms.NumberInput(
                attrs={
                    'class': "form-control",
                }),
            'department': forms.TextInput(
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
            'dni': forms.NumberInput(
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
            'NSA_code': forms.TextInput(
                attrs={
                    'class': "form-control",
                }),
        }
        labels = {
            'name': 'Nombre:',
            'surnames': 'Apellidos:',
            'num_carnet': 'N° carnet:',
            'birthdate': 'Fecha de nacimiento:',
            'department': 'Departamento:',
            'military_card': 'N° de libreta militar:',
            'province': 'Provincia:',
            'profession': 'Profesión:',
            'activity': 'Actividad:',
            'degree_instruction': 'Grado de instrucción:',
            'civil_status': 'Estado civil:',
            'dni': 'Numero de Dni:',
            'address': 'Dirección:',
            'phone': 'N° de teléfono:',
            'num_promotion': 'N° de promoción:',
            'promotion_delegate': 'Delegado de promoción:',
            'NSA_code': 'Código NSA:',
        }

class PartnerDetailForm(forms.ModelForm):
    
    class Meta:
        
        model = Partner
        fields = ['name', 'surnames', 'birthdate', 'num_carnet', 'dni', 'military_card', 'province', 'department', 'address', 'district',
                  'activity',
                  'degree_instruction', 'civil_status', 'dni', 'profession', 'phone', 'num_promotion', 'NSA_code', 'promotion_delegate']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled',
                }),
            'surnames': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled',
                }),
            'birthdate': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'num_carnet': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'military_card': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'department': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'province': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'address': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'district': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'profession': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),

            'activity': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'degree_instruction': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'civil_status': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'dni': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),

            'phone': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'num_promotion': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
            'promotion_delegate': forms.CheckboxInput(
                attrs={
                    'type': "checkbox",
                    'class': "form-check-input",
                    'disabled': 'disabled',
                }),
            'NSA_code': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'disabled': 'disabled',
                }),
        }
        labels = {
            'name': 'Nombre:',
            'surnames': 'Apellidos:',
            'num_carnet': 'N° carnet:',
            'birthdate': 'Fecha de nacimiento:',
            'department': 'Departamento:',
            'military_card': 'N° de libreta militar:',
            'province': 'Provincia:',
            'profession': 'Profesión:',
            'activity': 'Actividad:',
            'degree_instruction': 'Grado de instrucción:',
            'civil_status': 'Estado civil:',
            'dni': 'Numero de Dni:',
            'address': 'Dirección:',
            'phone': 'N° de teléfono:',
            'num_promotion': 'N° de promoción:',
            'promotion_delegate': 'Delegado de promoción:',
            'NSA_code': 'Código NSA:',
        }
