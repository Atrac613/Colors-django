from django.conf.urls import patterns, include, url

from colors.apps.frontend.views import index as defaultIndexPage
from colors.apps.frontend.views import test as testPage
from colors.apps.frontend.views import view as viewPage
from colors.apps.frontend.views import find as findPage
from colors.apps.api.views import upload as uploadAPI

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'colors.views.home', name='home'),
    # url(r'^colors/', include('colors.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', defaultIndexPage),
    (r'^test$', testPage),
    (r'^api/upload$', uploadAPI),
    (r'^p/(?P<page_id>\w+)$', viewPage),
    (r'^f/(?P<color_id>\w+)$', findPage),
)
