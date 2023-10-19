import django_filters
from .models import Partner
from django import forms


class PartnerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Nombre', field_name='name',
                                     lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surnames = django_filters.CharFilter(label='Apellido', field_name='surnames',
                                         lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = django_filters.NumberFilter(
        label='Dni', field_name='dni', lookup_expr='icontains', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Partner
        fields = ['name', 'surnames', 'dni']
