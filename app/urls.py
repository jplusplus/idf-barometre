from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^partial/(?P<partial_name>(\w+))\.html$', 'app.barometre.views.partial',       name='partial'),
    url(r'^$',                                      'app.barometre.views.home',          name='home'),
    url(r'^answers\.(?P<format>(json|csv))$',       'app.barometre.views.answers',       name='answers'),
    url(r'^introductions.json$',                    'app.barometre.views.introductions', name='introductions'),
    url(r'^admin/',                                 include(admin.site.urls)),
)
