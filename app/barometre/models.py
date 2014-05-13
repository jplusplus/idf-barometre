# -*- coding: utf-8 -*-
from django.db                 import models
from django.conf               import settings 
from django.utils.html         import strip_tags
from django.core.files.storage import FileSystemStorage
from dateutil.relativedelta    import relativedelta
from django.utils.text         import truncate_words
import datetime
import pytz
import re


fs = FileSystemStorage(location=settings.MEDIA_ROOT)
# Create your models here.
IMPORT_MODELS = (
    ('barometre.Profil',   'Profils',),
    ('barometre.Question', 'Questions',),
    ('barometre.Answer',   'Réponses',),
)

IMPORT_DELIMITERS = (
    (',',  'virgule',),
    (';',  'point-virgule',),
    ("\t", 'tabulation',),
)

IMPORT_DATEFORMATS = (
    ('%d/%m/%y', 'jj/mm/aa',),
    ('%d/%m/%Y', 'jj/mm/aaaa',),
    ('%y/%m/%d', 'aa/mm/jj',),
    ('%Y/%m/%d', 'aaaa/mm/jj',),    
    ('%m/%y',    'mm/aa',),
    ('%m/%Y',    'mm/aaaa',),
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
    format    = models.CharField(max_length=128, blank=False, choices=INTRO_FORMATS, default='simple')
    sentence  = models.TextField(blank=True, 
                                verbose_name='Phrase',
                                help_text='Exemple: Que pensent les <strong>ouvriers</strong> des <strong>transports en commun</strong> ?')
    # related_name='+' disable backward relation
    profil    = models.ForeignKey(Profil, related_name='+')
    question  = models.ForeignKey(Question, related_name='+')    
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
        sentence  = strip_tags(self.sentence)
        if type(indicator) in (int,str,):
            return '%s %s' % (indicator, sentence)        
        elif "value" in indicator:
            return '%s %s' % (indicator["value"], sentence)                    
        else:
            return sentence

    def profil_truncated(self):
        return truncate_words(self.profil.display, 4)

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
                    delta = Answer.normalize_date(currentAnswer[0].date - relativedelta(months=2))
                else:
                    # Previous answer date by default: 1 year before
                    delta = currentAnswer[0].date - relativedelta(years=1)

                filters["date__month"] = delta.month
                filters["date__year"]  = delta.year
                # Get the previous answer
                previousAnswer = Answer.objects.order_by("-date").filter(**filters)                          

                # The revious answer exists
                if previousAnswer:
                    indicator["value"]    = Answer.float( currentAnswer[0].ratio - previousAnswer[0].ratio, "pt", "pts")
                    indicator["current"]  = Answer.float( currentAnswer[0].ratio, "%")
                    indicator["previous"] = Answer.float( previousAnswer[0].ratio, "%")
                    indicator["class"]    = "increase" if currentAnswer[0].ratio >= previousAnswer[0].ratio else "decrease" 
                
        return indicator


class Answer(models.Model):
    date              = models.DateTimeField()
    # related_name='+' disable backward relation
    question          = models.ForeignKey(Question, related_name='+')    
    profil            = models.ForeignKey(Profil, related_name='+')
    ratio             = models.FloatField(help_text="Ratio assez satisfait et très satisfait", blank=True, null=True)
    ratio_unsatisfied = models.FloatField(help_text="Ratio pas vraiment satisfaite et pas du tout satisfait", blank=True, null=True)
    created_at        = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)

    class Meta:
        verbose_name        = u"réponse"
        verbose_name_plural = u"réponses"

    def __unicode__(self):
        date = self.local_date().strftime("%m/%Y")
        return  u'%s: Question "%s" selon %s' % (date, self.question.display, self.profil.display) 
    
    def local_date(self):
        return Answer.normalize_date(self.date)

    @staticmethod    
    def float(val, suffix_single='', suffix_plural=''):
        # Take the single suffix as default valure for plural suffix
        suffix_plural = suffix_single if suffix_plural == '' else suffix_plural
        # Create the right suffix
        suffix = suffix_plural if val > 1 or val < -1 else suffix_single
        return str( round(val, 1) ).replace('.', ',') + suffix

    @staticmethod   
    def normalize_date(date):
        paris_tz = pytz.timezone("Europe/Paris")
        return paris_tz.normalize(date)


class Import(models.Model):
    model_name  = models.CharField(max_length=255, blank=False, choices=IMPORT_MODELS, default='barometre.Answer')
    upload_file = models.FileField(upload_to='csv', storage=fs, help_text="Fichier utilisé pour importer des données.", verbose_name="Fichier à uploader")
    delimiter   = models.CharField(max_length=56, blank=False, choices=IMPORT_DELIMITERS, default=';', help_text="Délimiteur dans le fichier CSV.", verbose_name="Délimiteur")
    dateformat  = models.CharField(max_length=56, blank=False, choices=IMPORT_DATEFORMATS, default='%d/%m/%y', help_text="Format des dates dans le fichier.", verbose_name="Format des dates")
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
        