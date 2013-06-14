from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^partial/(?P<partial_name>(\w+))\.html$', 'barometre.views.partial', name='partial'),
    url(r'^$',                                      'barometre.views.home',    name='home'),
    url(r'^data\.(?P<format>(json|csv))$',          'barometre.views.data',    name='data'),
    url(r'^admin/',                                 include(admin.site.urls)),
)
