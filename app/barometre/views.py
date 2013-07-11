#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template        import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts       import render_to_response, redirect
from django.http            import Http404, HttpResponse
from django.core            import serializers
from django.db.models       import Max, Min
from random                 import random, shuffle
from app.barometre.models   import Answer, Introduction, Profil


import csv
import json
import pytz
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
    # Paris timezone to normalize the date
    paris_tz = pytz.timezone("Europe/Paris")
    # now extract the inner 'fields' into profil and question
    # and simplify the date field
    for index, row in enumerate(actual_data):
        row["date"]     = paris_tz.normalize(row["date"]).strftime("%m/%Y")
        row["profil"]   = row["profil"]["fields"]["display"]
        row["question"] = row["question"]["fields"]["display"]
        # Useless value
        del row["created_at"]

    # JSON request
    if format == 'json':   
        # Maximun and minimun ratios to calculate the graph scale
        minRatio = 0
        maxRatio = 100
        # Change them only if we received a question filter
        if "question" in request.GET:
            # Get all answers for this question
            answers  = Answer.objects.filter(question__slug=request.GET["question"])
            # Aggregates the minimun and maximum ratios
            question_min = answers.aggregate(Min('ratio'))["ratio__min"]
            question_max = answers.aggregate(Max('ratio'))["ratio__max"]

        # Create rows subset to embed min and max values   
        data = { 
            "rows": actual_data,
            "question_min" : question_min,
            "question_max" : question_max
        }
        # and now dump to JSON
        output = json.dumps(data, default=dthandler)    
        # Returns the data as JSON type
        return HttpResponse(output, mimetype="application/json")
    # CSV request
    elif format == 'csv':        
        filename = "answers"
        if "question" in request.GET:
            filename += "-" + request.GET["question"]
        if "profil" in request.GET:
            filename += "-" + request.GET["profil"]            
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/text')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (filename,)
        # Frist the answer
        writer = csv.writer(response)
        # Only if there is data
        if len(actual_data) > 0:
            # Take the first row keys as header
            writer.writerow( actual_data[0].keys() )
            # Take every row values
            for row in actual_data:
                # UT8 encode the string
                values = [unicode(s).encode("utf-8") for s in row.values()]
                # Add the encoded values to the CSV
                writer.writerow( values )

        # Returns the data as CSV type
        return response
    else:
        raise Http404


def introductions(request):  
    introductions = list()
    alls = Introduction.objects.order_by("?")

    questions = ['transport', 'economique', 'environnement']
    formats   = ['simple', 'proportion', 'number']
    profils   = Profil.objects.all().order_by("?")
    # Randomize the data set
    shuffle(questions)

    # Get introductions for each profil and type
    for p in profils:
        count = 0        
        for q in questions:
            # Only 3 by question
            if len([i for i in introductions if i.question.slug == q]) < 3:
                # Random formats order
                shuffle(formats)
                # Look for an intro for this question in each format
                for f in formats:
                    if count < 1:            
                        filters = dict(question__slug=q, profil=p, format=f)
                        dataset = alls.filter(**filters)
                        if dataset:
                            introductions.append( dataset[0] )
                            count = count+1
        # Break upside 9 introductions
        if len(introductions) >= 9:
            break

    # Do not take more than 9 rows
    introductions = introductions[0:9]    

    # First and last element of the list must be in trend format
    indexes = (0, len(introductions)-1)
    for idx in indexes:
        # Get the introduction
        q = introductions[idx].question.slug
        # And choose a trend one, for the same question
        intro = alls.filter(question__slug=q, format="trend")
        if intro:
            introductions[idx] = intro[0]

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

