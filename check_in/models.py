from django.db import models

class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ('created',)
