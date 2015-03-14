import django_filters
import django_select2

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset

from core.models import (
    Article,
    User,
)


class ArticleChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Article.objects.all()
    search_fields = ['description__icontains', 'title__icontains']


class UserChoiceField(django_select2.AutoModelSelect2Field):
    queryset = User.objects.all()
    search_fields = ['email__icontains']


class ArticleChoiceFilter(django_filters.Filter):
    field_class = ArticleChoiceField


class UserChoiceFilter(django_filters.Filter):
    field_class = UserChoiceField


class ArticleListViewFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(ArticleListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Article

        fields = [u'description']

        exclude = []


class UserListViewFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(UserListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = User

        fields = ['email', ]

        exclude = []

# Have to call it clearly to help django_select2 register fields
ArticleChoiceField()
UserChoiceField()
