#!/usr/bin/env python
# Encoding: utf-8

from django.template        import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts       import render_to_response, redirect
from django.http            import Http404, HttpResponse
from django.core            import serializers
from app.barometre.models   import Answer, Introduction
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

def answers(request, format='json'):    
    # Build filters
    filters = {}
    if "question" in request.GET:
        filters["question__slug"] = request.GET["question"]
    if "profil" in request.GET:
        filters["profil__slug"] = request.GET["profil"]

    # Get the answers ordering by date
    answers = Answer.objects.exclude(ratio__lte=0).filter(**filters).order_by("date")

    if format == 'json':                
        # this gives you a list of dicts
        raw_data = serializers.serialize('python', answers, relations=('profil','question',))
        # now extract the inner `fields` dicts
        actual_data = [d['fields'] for d in raw_data]
        # now extract the inner 'fields' into profil and question
        # and simplify the date field
        for index, row in enumerate(actual_data):
            row["date"]     = row["date"].strftime("%m/%Y")
            row["profil"]   = row["profil"]["fields"]["display"]
            row["question"] = row["question"]["fields"]["display"]
        # and now dump to JSON
        output = json.dumps(actual_data, default=dthandler)    

        return HttpResponse(output, mimetype="application/json")
    else:
        return Http404


def introductions(request):
    # Get the introductions ordering by date
    introductions = Introduction.objects.all()
    # Serialize data
    raw_data = serializers.serialize('python', introductions, relations=('profil','question'), extras=("indicator",))
    # now extract the inner 'fields' and 'extras' dicts
    actual_data = [dict(d['fields'].items() + d['extras'].items()) for d in raw_data]
    # and simplify some field
    for index, row in enumerate(actual_data):                   
        row["profil"]    = row["profil"]["fields"]
        row["question"]  = row["question"]["fields"]     
        row["indicator"] = eval(row["indicator"])   
            
    # and now dump to JSON
    output = json.dumps(actual_data, default=dthandler)    

    return HttpResponse(output, mimetype="application/json")

