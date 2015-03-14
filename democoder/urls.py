from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '', url(r'^$', RedirectView.as_view(pattern_name="article-list")),
    url(r'^core/', include('apps.core.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^payments/', include('djstripe.urls', namespace="djstripe")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ext/', include('django_select2.urls')),)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
