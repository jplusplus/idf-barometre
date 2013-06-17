# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings 
from django.core.files.storage import FileSystemStorage
import re


TAXO_WHAT = (
    ('0', 'question'),
    ('1', 'profil'),
)

fs = FileSystemStorage(location=settings.MEDIA_ROOT)
# Create your models here.
IMPORT_MODELS = (
    ('barometre.Taxonomy', 'Catégories',),
    ('barometre.Answer',   'Réponses',),
)

class Taxonomy(models.Model):
    display  = models.CharField(max_length=200)
    slug     = models.SlugField(max_length=200)
    aliases  = models.CharField(max_length=600)
    what     = models.CharField(max_length=40, choices=TAXO_WHAT, default='1')
    created_at  = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)
    class Meta:
        verbose_name        = u"catégorie"
        verbose_name_plural = u"catégories"
    def __unicode__(self):
        return  self.display

class Answer(models.Model):
    date       = models.DateTimeField()
    # related_name='+' disable backward relation
    question   = models.ForeignKey(Taxonomy, related_name='+')    
    profil     = models.ForeignKey(Taxonomy, related_name='+')
    ratio      = models.FloatField()
    created_at = models.DateTimeField(null=True, auto_now_add=True, db_column='created_at', blank=True)

    class Meta:
        verbose_name        = u"réponse"
        verbose_name_plural = u"réponses"
    def __unicode__(self):
        date = self.date.strftime("%m/%Y")
        return  u'%s: Question "%s" selon %s' % (date, self.question, self.profil) 

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
        