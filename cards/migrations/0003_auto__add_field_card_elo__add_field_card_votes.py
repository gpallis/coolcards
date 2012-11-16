# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Card.elo'
        db.add_column('cards_card', 'elo',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'Card.votes'
        db.add_column('cards_card', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Card.elo'
        db.delete_column('cards_card', 'elo')

        # Deleting field 'Card.votes'
        db.delete_column('cards_card', 'votes')


    models = {
        'cards.card': {
            'Meta': {'object_name': 'Card'},
            'elo': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['cards']