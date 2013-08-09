# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.description'
        db.add_column(u'check_in_entry', 'description',
                      self.gf('django.db.models.fields.TextField')(default=datetime.datetime(2013, 8, 7, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entry.description'
        db.delete_column(u'check_in_entry', 'description')


    models = {
        u'check_in.entry': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Entry'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['check_in']