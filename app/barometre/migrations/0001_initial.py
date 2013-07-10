# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profil'
        db.create_table('barometre_profil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('aliases', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='created_at', blank=True)),
        ))
        db.send_create_signal('barometre', ['Profil'])

        # Adding model 'Question'
        db.create_table('barometre_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('aliases', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='created_at', blank=True)),
        ))
        db.send_create_signal('barometre', ['Question'])

        # Adding model 'Introduction'
        db.create_table('barometre_introduction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('format', self.gf('django.db.models.fields.CharField')(default='simple', max_length=128)),
            ('sentence', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('profil', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['barometre.Profil'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['barometre.Question'])),
            ('variation', self.gf('django.db.models.fields.CharField')(default='simple', max_length=128, blank=True)),
        ))
        db.send_create_signal('barometre', ['Introduction'])

        # Adding model 'Answer'
        db.create_table('barometre_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['barometre.Question'])),
            ('profil', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['barometre.Profil'])),
            ('ratio', self.gf('django.db.models.fields.FloatField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='created_at', blank=True)),
        ))
        db.send_create_signal('barometre', ['Answer'])

        # Adding model 'Import'
        db.create_table('barometre_import', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(default='barometre.Answer', max_length=255)),
            ('upload_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('encoding', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('error_log', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_column='created_at', blank=True)),
        ))
        db.send_create_signal('barometre', ['Import'])

    def backwards(self, orm):
        # Deleting model 'Profil'
        db.delete_table('barometre_profil')

        # Deleting model 'Question'
        db.delete_table('barometre_question')

        # Deleting model 'Introduction'
        db.delete_table('barometre_introduction')

        # Deleting model 'Answer'
        db.delete_table('barometre_answer')

        # Deleting model 'Import'
        db.delete_table('barometre_import')


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