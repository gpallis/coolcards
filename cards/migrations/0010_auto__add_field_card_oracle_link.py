# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Card.oracle_link'
        db.add_column('cards_card', 'oracle_link',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cards.Oracle'], unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Card.oracle_link'
        db.delete_column('cards_card', 'oracle_link_id')


    models = {
        'cards.card': {
            'Meta': {'ordering': "['-elo', 'name']", 'object_name': 'Card'},
            'elo': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oracle_link': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cards.Oracle']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cards.oracle': {
            'Meta': {'ordering': "['name']", 'object_name': 'Oracle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'power': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'rules': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True'}),
            'toughness': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cards']