from django.conf      import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.barometre',    
    url(r'^partial/(?P<partial_name>(\w+))\.html$', 'views.partial',       name='partial'),
    url(r'^$',                                      'views.home',          name='home'),
    url(r'^answers\.(?P<format>(json|csv))$',       'views.answers',       name='answers'),
    url(r'^introductions.json$',                    'views.introductions', name='introductions'),   
)