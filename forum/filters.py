import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from django.forms.widgets import TextInput
from django_ckeditor_5.fields import CKEditor5Field  # Ensure this is a valid import



from . models import *

# On forum we have filters to be able to filter posts, that we like to see.
# this code is responsible for basic funcitonality of filter

class ForumFilter(django_filters.FilterSet):

	id = NumberFilter(label="ID", field_name='id', lookup_expr='exact')
	name = CharFilter(label="Name", field_name='name', lookup_expr='icontains', widget=TextInput(attrs={'placeholder':'Name'}))
	user_username = CharFilter(label="Author", field_name='user__username',lookup_expr='icontains', widget=TextInput(attrs={'placeholder':'Author'}))
	
	topic = CharFilter(label="Topic", field_name='topic', lookup_expr='icontains', widget=TextInput(attrs={'placeholder':'Topic'}))
	# icontains like where query
	tags = CharFilter(label="Tags", field_name='tags', lookup_expr='slug__icontains', widget=TextInput(attrs={'placeholder':'Tags'}))
	text = CharFilter(label="Text Contains", field_name='text', lookup_expr='icontains', widget=TextInput(attrs={'placeholder':'Text contains'}))

	lessrating = NumberFilter(label="Rating", field_name='post_reputation', lookup_expr='lte')
	rating = NumberFilter(label="Rating", field_name='post_reputation', lookup_expr='exact')
	greatrating = NumberFilter(label="Rating", field_name='post_reputation', lookup_expr='gte')

	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')

# This is advanced forum filter form

class ForumAdvancedFilter(django_filters.FilterSet):
	user_username = CharFilter(label="Author", field_name='user__username',lookup_expr='icontains', widget=TextInput(attrs={'placeholder':'Author'}))
	class Meta:
		model = ForumPost
		fields = '__all__'
		filter_overrides = {
            TaggableManager: {'filter_class': CharFilter},
            CKEditor5Field: {
                'filter_class': CharFilter,  # Use CharFilter for CKEditor5Field
                'lookup_expr': 'icontains',  # You can change the lookup expression if needed
            },
        }