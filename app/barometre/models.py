# -*- coding: utf-8 -*-
from django.db                 import models
from django.conf               import settings 
from django.utils.html         import strip_tags
from django.core.files.storage import FileSystemStorage
from dateutil.relativedelta    import relativedelta
import datetime
import re


fs = FileSystemStorage(location=settings.MEDIA_ROOT)
# Create your models here.
IMPORT_MODELS = (
    ('barometre.Profil',   'Profils',),
    ('barometre.Question', 'Questions',),
    ('barometre.Answer',   'Réponses',),
)

# Formats of introductions
INTRO_FORMATS = (
    ('simple', 'Question sans chiffre',),
    ('proportion', 'Part d\'une population',),
    ('number', 'Nombre de françiliens',),
    ('trend', 'Taux de croissance',),
)

# Variaof the 
INTRO_VARIATIONS = (
    ('last_2_month', '2 derniers mois',),
    ('last_year', '1 an',),
)

# Number of franciliens
NB_FRANCILIENS_M = 11.8


class Profil(models.Model):
    display    = models.CharField(max_length=200)
    slug       = models.SlugField(max_length=200)
    aliases    = models.CharField(max_length=600)
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)
    class Meta:
        verbose_name        = u"profil"
        verbose_name_plural = u"profils"

    def __unicode__(self):
        return self.display

class Question(models.Model):
    display    = models.CharField(max_length=200)
    slug       = models.SlugField(max_length=200)
    aliases    = models.CharField(max_length=600)
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)
    class Meta:
        verbose_name        = u"question"
        verbose_name_plural = u"questions"

    def __unicode__(self):
        return self.display


class Introduction(models.Model):
    sentence  = models.TextField(blank=True, 
                                verbose_name='Phrase',
                                help_text='Exemple: Que pensent les <strong>ouvriers</strong> des <strong>transports en commun</strong> ?')
    # related_name='+' disable backward relation
    profil    = models.ForeignKey(Profil, related_name='+')
    question  = models.ForeignKey(Question, related_name='+')    
    format    = models.CharField(max_length=128, blank=False, choices=INTRO_FORMATS, default='simple')
    variation = models.CharField(max_length=128, 
                                 blank=True, 
                                 choices=INTRO_VARIATIONS,
                                 default='simple',
                                 help_text='Seulement pour les taux de croissance.')
    class Meta:
        verbose_name        = u"phrase d'introduction"
        verbose_name_plural = u"phrases d'introduction"

    def __unicode__(self):
        indicator = self.indicator()
        if type(indicator) in (int,str,):
            return '%s %s' % (indicator, self.sentence)        
        elif "value" in indicator:
            return '%s %s' % (indicator["value"], self.sentence)                    
        else:
            return self.sentence

    def indicator(self):
        # Default indicator to None
        indicator = dict()
        # Filter the answers to the selected sample             
        filters = {'question':self.question, 'profil':self.profil}
        # Find the proportion
        if self.format == 'proportion':            
            # Get the answer
            answer = Answer.objects.order_by("-date").filter(**filters)
            # Do we found an answer ?
            if answer:
                # Aake the first row and add a percentage 
                indicator["value"] = Answer.float( answer[0].ratio, "%")
        # Find the quantity
        elif self.format == 'number':
            # Get the answer
            answer = Answer.objects.order_by("-date").filter(**filters)
            # Do we found an answer ?
            if answer:
                # Aake the first row and add a percentage 
                indicator["value"] = Answer.float( NB_FRANCILIENS_M*answer[0].ratio/100 )
        # Find a trend
        elif self.format == 'trend':
            # Current answer
            currentAnswer = Answer.objects.order_by("-date").filter(**filters)            
            # Do we find the current value?
            if currentAnswer:                    
                # Update the filter according the variation field
                if self.variation == 'last_2_month':                                 
                    # Previous answer date: 2 month before
                    filters["date"] = currentAnswer[0].date - relativedelta(months=2)
                else:
                    # Previous answer date by default: 1 year before
                    filters["date"] = currentAnswer[0].date - relativedelta(years=1)

                # Get the previous answer
                previousAnswer = Answer.objects.order_by("-date").filter(**filters)                 
                # The revious answer exists
                if previousAnswer:
                    indicator["value"]    = Answer.float( currentAnswer[0].ratio - previousAnswer[0].ratio, "%")
                    indicator["current"]  = Answer.float( currentAnswer[0].ratio, "%")
                    indicator["previous"] = Answer.float( previousAnswer[0].ratio, "%")
                
        return indicator


class Answer(models.Model):
    date       = models.DateTimeField()
    # related_name='+' disable backward relation
    question   = models.ForeignKey(Question, related_name='+')    
    profil     = models.ForeignKey(Profil, related_name='+')
    ratio      = models.FloatField()
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)

    class Meta:
        verbose_name        = u"réponse"
        verbose_name_plural = u"réponses"

    def __unicode__(self):
        date = self.date.strftime("%m/%Y")
        return  u'%s: Question "%s" selon %s' % (date, self.question.display, self.profil.display) 

    @staticmethod    
    def float(val, suffix=''):
        return str( round(val, 1) ).replace('.', ',') + suffix

class Import(models.Model):
    model_name  = models.CharField(max_length=255, blank=False, choices=IMPORT_MODELS, default='barometre.Answer')
    upload_file = models.FileField(upload_to='csv', storage=fs)
    file_name   = models.CharField(max_length=255, blank=True)
    encoding    = models.CharField(max_length=32, blank=True)  
    error_log   = models.TextField(help_text='Each line is an import error')
    created_at  = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)

    class Meta:
        verbose_name        = u"importation"
        verbose_name_plural = u"importations"

    def error_log_html(self):
        return re.sub('\n', '<br/>', self.error_log)

    error_log_html.allow_tags = True

    def __unicode__(self):
        return self.upload_file.name
        