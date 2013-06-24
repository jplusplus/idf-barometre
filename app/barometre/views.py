#!/usr/bin/env python
# Encoding: utf-8

from django.template        import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts       import render_to_response, redirect
from django.http            import Http404, HttpResponse
from django.core            import serializers
from random                 import random, shuffle
from app.barometre.models   import Answer, Introduction


import csv
import json
import datetime

# Merge severals lists
from itertools import chain
merge = lambda l1, l2: list(chain(l1, l2)) 
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
        # Useless value
        del row["created_at"]

    # JSON request
    if format == 'json':                
        # and now dump to JSON
        output = json.dumps(actual_data, default=dthandler)    
        # Returns the data as JSON type
        return HttpResponse(output, mimetype="application/json")
    # CSV request
    elif format == 'csv':        
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/text')
        response['Content-Disposition'] = 'attachment; filename="answer.csv"'
        # Frist the answer
        writer = csv.writer(response)
        # Only if there is data
        if len(actual_data) > 0:
            # Take the first row keys as header
            writer.writerow( actual_data[0].keys() )
            # Take every row values
            for row in actual_data:
                writer.writerow( row.values() )

        # Returns the data as CSV type
        return response
    else:
        raise Http404


def introductions(request):  
    # Index of the set with 3 simple blocks
    rand = int(random()*2.9)
    # Determines the length of each set
    transport_len     = 3 if rand == 0 else 2 
    economique_len    = 3 if rand == 1 else 2 
    environnement_len = 3 if rand == 2 else 2 
    # First get all small introductions
    smalls = Introduction.objects.exclude(format="trend").order_by("?")
    # Get the introductions ordering by date.
    # Pick 2 elements for two of the sets,
    # 3 elements for the third one
    # (according the previous numbers)
    transport     = smalls.filter(question__slug="transport")[:transport_len]
    economique    = smalls.filter(question__slug="economique")[:economique_len]
    environnement = smalls.filter(question__slug="environnement")[:environnement_len]
    # Merge and the 3 data sets
    introductions = merge(transport, merge(economique, environnement))
    # Shuffle the dataset
    shuffle(introductions)
    # Now pick 2 bigs introductions for the datasets with only 2 elements  
    bigs = Introduction.objects.filter(format='trend').order_by("?")    
    big_intros = list()

    if transport_len == 2:
        transport = bigs.filter(question__slug="transport")        
        if transport : big_intros.append(transport[0]) 

    if economique_len == 2:
        economique = bigs.filter(question__slug="economique")        
        if economique : big_intros.append(economique[0]) 

    if environnement_len == 2:
        environnement = bigs.filter(question__slug="environnement")        
        if environnement : big_intros.append(environnement[0]) 
    
    # Shuffle big rows
    shuffle(big_intros)
    bigs_len = len(big_intros);
    # Then append the big intro to right position
    if bigs_len > 0: introductions.insert(0, big_intros[0])
    if bigs_len > 1: introductions.insert(8, big_intros[1])

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

