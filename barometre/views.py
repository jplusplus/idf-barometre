#!/usr/bin/env python
# Encoding: utf-8

from django.template        import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts       import render_to_response, redirect
from django.http            import Http404

def home(request):
    locales = {}
    return render_to_response('home.dj.html', locales, context_instance=RequestContext(request))

def partial(request, partial_name=None):    
    locales = {}
    template_name = 'partials/' + partial_name + '.dj.html';
    try:
        return render_to_response(template_name, locales, context_instance=RequestContext(request))    
    except TemplateDoesNotExist:
        raise Http404