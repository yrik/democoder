from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView
from allauth.account.utils import complete_signup

from .decorators import ForbiddenUser

from .forms import LoginForm
from .forms import SignUpUserForm

from core.models import (
    Article,
    User,
)
from core.forms import (
    ArticleCreateForm,
)

from core.filters import (
    ArticleListViewFilter,
    UserListViewFilter,
)


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class ArticleCreateView(CreateView):

    """Article create view"""
    model = Article
    form_class = ArticleCreateForm
    template_name = "article-create.html"

    def get_success_url(self):
        messages.success(self.request, _("Article succesfully created"))
        return reverse("article-list", args=[])


class ArticleListView(OrderableListMixin, ListFilteredView, PaginationMixin):

    """Article list view"""
    model = Article
    template_name = "article-list.html"
    paginate_by = 10
    orderable_columns = ["description", "title", ]
    orderable_columns_default = "id"
    filter_set = ArticleListViewFilter


def auth(request):
    login_form = LoginForm()
    signup_form_user = SignUpUserForm(prefix="user", request=request)

    redirect_url = '/'
    redirect_url = request.GET.get('next', redirect_url)

    if request.method == 'POST' and 'login_form' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return login_form.login(request, redirect_url=redirect_url)

    if request.method == 'POST' and 'signup_user_form' in request.POST:
        signup_form_user = SignUpUserForm(
            request.POST,
            prefix="user",
            request=request)

        if signup_form_user.is_valid():
            user = signup_form_user.save(request)
            return complete_signup(request, user, False, redirect_url)

    return render(request, "auth.html", {
        "login_form": login_form,
        "signup_form_user": signup_form_user,
    })
