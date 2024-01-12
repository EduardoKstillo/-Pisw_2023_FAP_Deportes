import django_filters
from .models import Person, Team
from django import forms


class PersonFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Nombre', field_name='name',
                                     lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surnames = django_filters.CharFilter(label='Apellido', field_name='surnames',
                                         lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = django_filters.NumberFilter(
        label='Dni', field_name='dni', lookup_expr='icontains', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Person
        fields = ['name', 'surnames', 'dni']


class TeamFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(
        label='Categoria', field_name='category', lookup_expr='icontains', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Team
        fields = ['category']
