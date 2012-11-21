# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table('activity_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('voter', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('voted_for', self.gf('django.db.models.fields.related.ForeignKey')(related_name='card_voted_for_set', to=orm['cards.Card'])),
            ('voted_against', self.gf('django.db.models.fields.related.ForeignKey')(related_name='card_voted_against_set', to=orm['cards.Card'])),
        ))
        db.send_create_signal('activity', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table('activity_vote')


    models = {
        'activity.vote': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'voted_against': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_voted_against_set'", 'to': "orm['cards.Card']"}),
            'voted_for': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_voted_for_set'", 'to': "orm['cards.Card']"}),
            'voter': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'cards.card': {
            'Meta': {'ordering': "['-elo']", 'object_name': 'Card'},
            'elo': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pic_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['activity']