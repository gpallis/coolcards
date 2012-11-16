# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Card.pic_url'
        db.add_column('cards_card', 'pic_url',
                      self.gf('django.db.models.fields.CharField')(default='http://magiccards.info/scans/en/wwk/31.jpg', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Card.pic_url'
        db.delete_column('cards_card', 'pic_url')


    models = {
        'cards.card': {
            'Meta': {'object_name': 'Card'},
            'elo': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pic_url': ('django.db.models.fields.CharField', [], {'default': "'http://magiccards.info/scans/en/wwk/31.jpg'", 'max_length': '200'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['cards']