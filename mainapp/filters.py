import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter
from django.forms.widgets import TextInput

from . models import *

# This filter file contains basic functionality for our news filtering options 

class newsFilter(django_filters.FilterSet):
	name = CharFilter(label="", field_name='name', lookup_expr='icontains', widget=TextInput(attrs={'placeholder':'Name'}))
	start_date = DateFilter(label="", field_name="date_created", lookup_expr='gte', widget=TextInput(attrs={'placeholder':'Date from, e.g.: 2020-12-03'}))
	end_date = DateFilter(label="", field_name="date_created", lookup_expr='lte', widget=TextInput(attrs={'placeholder':'End date, e.g.: 2022-08-04'}))
