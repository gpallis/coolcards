# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Oracle.power'
        db.add_column('cards_oracle', 'power',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Oracle.toughness'
        db.add_column('cards_oracle', 'toughness',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Oracle.power'
        db.delete_column('cards_oracle', 'power')

        # Deleting field 'Oracle.toughness'
        db.delete_column('cards_oracle', 'toughness')


    models = {
        'cards.card': {
            'Meta': {'ordering': "['-elo']", 'object_name': 'Card'},
            'elo': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pic_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cards.oracle': {
            'Meta': {'ordering': "['name']", 'object_name': 'Oracle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'power': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rules': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True'}),
            'toughness': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cards']