# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'storelocator_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'storelocator', ['Location'])

        # Adding model 'StoreLocator'
        db.create_table(u'storelocator_storelocator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=55)),
        ))
        db.send_create_signal(u'storelocator', ['StoreLocator'])

        # Adding model 'Shop'
        db.create_table(u'storelocator_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('storelocator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shops', to=orm['storelocator.StoreLocator'])),
        ))
        db.send_create_signal(u'storelocator', ['Shop'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'storelocator_location')

        # Deleting model 'StoreLocator'
        db.delete_table(u'storelocator_storelocator')

        # Deleting model 'Shop'
        db.delete_table(u'storelocator_shop')


    models = {
        u'storelocator.location': {
            'Meta': {'ordering': "['iso', 'postalcode']", 'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'storelocator.shop': {
            'Meta': {'object_name': 'Shop'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'storelocator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shops'", 'to': u"orm['storelocator.StoreLocator']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'storelocator.storelocator': {
            'Meta': {'object_name': 'StoreLocator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        }
    }

    complete_apps = ['storelocator']