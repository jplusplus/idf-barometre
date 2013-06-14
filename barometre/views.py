#!/usr/bin/env python
# Encoding: utf-8

from django.template        import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts       import render_to_response, redirect
from django.http            import Http404, HttpResponse
from django.core            import serializers
from barometre.models       import Answer
import csv
import json
import datetime

# Date handler for serialization
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

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

def data(request, format='json'):    
    # Build filters
    filters = {};
    if "question" in request.GET:
        filters["question__slug"] = request.GET["question"]
    if "profil" in request.GET:
        filters["profil__slug"] = request.GET["profil"]

    # Get the answers
    answers = Answer.objects.filter(**filters)

    if format == 'json':                
        # this gives you a list of dicts
        raw_data = serializers.serialize('python', answers, relations=('profil','question',))
        # now extract the inner `fields` dicts
        actual_data = [d['fields'] for d in raw_data]
        # now extract the inner 'fields' into profil and question
        for index, row in enumerate(actual_data):
            row["profil"]   = row["profil"]["fields"]["display"]
            row["question"] = row["question"]["fields"]["display"]
        # and now dump to JSON
        output = json.dumps(actual_data, default=dthandler)    

        return HttpResponse(output, mimetype="application/json")
    else:
        return Http404
