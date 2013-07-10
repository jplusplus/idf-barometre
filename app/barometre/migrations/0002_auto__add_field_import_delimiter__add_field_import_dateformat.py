# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Import.delimiter'
        db.add_column('barometre_import', 'delimiter',
                      self.gf('django.db.models.fields.CharField')(default=';', max_length=56),
                      keep_default=False)

        # Adding field 'Import.dateformat'
        db.add_column('barometre_import', 'dateformat',
                      self.gf('django.db.models.fields.CharField')(default='jj/mm/yy', max_length=56),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Import.delimiter'
        db.delete_column('barometre_import', 'delimiter')

        # Deleting field 'Import.dateformat'
        db.delete_column('barometre_import', 'dateformat')


    models = {
        'barometre.answer': {
            'Meta': {'object_name': 'Answer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'created_at'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['barometre.Profil']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['barometre.Question']"}),
            'ratio': ('django.db.models.fields.FloatField', [], {})
        },
        'barometre.import': {
            'Meta': {'object_name': 'Import'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'created_at'", 'blank': 'True'}),
            'dateformat': ('django.db.models.fields.CharField', [], {'default': "'jj/mm/yy'", 'max_length': '56'}),
            'delimiter': ('django.db.models.fields.CharField', [], {'default': "';'", 'max_length': '56'}),
            'encoding': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'error_log': ('django.db.models.fields.TextField', [], {}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'default': "'barometre.Answer'", 'max_length': '255'}),
            'upload_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'barometre.introduction': {
            'Meta': {'object_name': 'Introduction'},
            'format': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['barometre.Profil']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['barometre.Question']"}),
            'sentence': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'variation': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '128', 'blank': 'True'})
        },
        'barometre.profil': {
            'Meta': {'object_name': 'Profil'},
            'aliases': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'created_at'", 'blank': 'True'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        'barometre.question': {
            'Meta': {'object_name': 'Question'},
            'aliases': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_column': "'created_at'", 'blank': 'True'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['barometre']