from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from core.views import *


urlpatterns = patterns(
    '',
    url("^auth/$", auth, name="auth"),
    url(
        r'^aboutus/$',
        TemplateView.as_view(template_name='aboutus.html'),
        name="aboutus"
    ),
    url(
        r'^article-create/$',
        ArticleCreateView.as_view(),
        name="article-create"
    ),
    url(
        r'^article/list/$',
        ArticleListView.as_view(),
        name="article-list"
    ),
)
