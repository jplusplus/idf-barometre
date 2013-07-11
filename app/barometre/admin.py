# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.admin import ModelAdmin 
from redactor.widgets import AdminRedactorEditor
from app.barometre.models import Answer, Profil, Question, Import, Introduction

class TaxonomyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("display",)}
    list_display = ('display', 'slug',)

class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('question', 'profil', 'date')
    list_display = ('__unicode__', 'ratio', 'date', )

class IntroductionAdminForm(forms.ModelForm):    

    # Check that the profil
    # is set to "all" for the number format
    def clean_profil(self): 
        if self.cleaned_data["format"] == "number" and self.cleaned_data["profil"].slug != "all":
            raise forms.ValidationError(u"Le profil doit être \"total\" pour le format \"nombre de françiliens\".")
        return self.cleaned_data["profil"]   


    # Check that the variation is 
    # set only with "trend" format
    def clean_variation(self):      
        # Error, required value
        if self.cleaned_data["variation"] == "" and self.cleaned_data["format"] == "trend":
            raise forms.ValidationError(u"Une variation est requise pour le format \"taux de croissance\".")
        # Cleanup, empty this value if not "trend format"
        elif self.cleaned_data["variation"] != "" and self.cleaned_data["format"] != "trend":
            self.cleaned_data["variation"] = "" 
        return self.cleaned_data["variation"]
    
class IntroductionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'question', 'profil_truncated', 'format')
    list_filter = ('question', 'profil', 'format')
    form = IntroductionAdminForm
    formfield_overrides = {
        models.TextField: {'widget': AdminRedactorEditor(            
            redactor_settings={
                'overlay' : True,
                'buttons': [ 'bold', 'italic', 'deleted'],
                'autoformat': False,
            }
        )},
    }



class ImportAdmin(ModelAdmin):
    fields = ('upload_file', 'delimiter', 'dateformat')
    list_display = ('upload_file', 'model_name', 'created_at')

    formfield_overrides = {
        models.CharField: {
            'widget': forms.Textarea(attrs={'rows':'4', 'cols':'60'})
        },
    }

    def save_model(self, request, obj, form, change):
        """ Do save and process command - cant commit False
            since then file wont be found for reopening via right charset
        """
        form.save()
        from app.barometre.management.csvimport import Command
        cmd = Command()
        if obj.upload_file:
            obj.file_name = obj.upload_file.name
            obj.encoding = ''
            defaults = self.filename_defaults(obj.file_name)   
            cmd.setup(mappings=None,
                        modelname=obj.model_name, 
                        delimiter=obj.delimiter,
                        dateformat=obj.dateformat,
                        charset=obj.encoding,
                        uploaded=obj.upload_file,
                        defaults=defaults)
        
        errors = cmd.run(logid=obj.id)

        if errors:
            obj.error_log = '\n'.join(errors)

        obj.save()

    def filename_defaults(self, filename):
        """ Override this method to supply filename based data """
        defaults = []
        splitters = {'/':-1, '.':0, '_':0}
        for splitter, index in splitters.items():
            if filename.find(splitter)>-1:
                filename = filename.split(splitter)[index]
        return defaults

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Profil, TaxonomyAdmin)
admin.site.register(Question, TaxonomyAdmin)
admin.site.register(Introduction, IntroductionAdmin)    
admin.site.register(Import, ImportAdmin)    