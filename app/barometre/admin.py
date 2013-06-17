from datetime import datetime
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.admin import ModelAdmin 
from app.barometre.models import Answer, Taxonomy, Import

class TaxonomyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("display",)}
    list_display = ('display', 'what')

class AnswerAdmin(admin.ModelAdmin):
    pass

class ImportAdmin(ModelAdmin):
    fields = ['model_name','upload_file']
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
        from barometre.management.csvimport import Command
        cmd = Command()
        if obj.upload_file:
            obj.file_name = obj.upload_file.name
            obj.encoding = ''
            defaults = self.filename_defaults(obj.file_name)
            cmd.setup(mappings=None,
                        modelname=obj.model_name, 
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
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Import, ImportAdmin)    