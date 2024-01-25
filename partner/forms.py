from django import forms
from django.contrib.auth.models import Group
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
    def clean_groups(self):
        groups = self.cleaned_data['groups']
        return groups


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
