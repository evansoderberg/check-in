from rest_framework import serializers
from check_in.models import Entry
from django.conf import settings

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('city', 'description')    
