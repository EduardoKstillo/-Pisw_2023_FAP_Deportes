import django_filters
from .models import Team
from django import forms


class TeamFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(
        label='Categoria', field_name='category', lookup_expr='icontains', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Team
        fields = ['category']
