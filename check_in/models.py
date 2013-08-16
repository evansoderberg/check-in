from django.db import models

class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)
    description = models.TextField()
    ip = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    image = models.ImageField(upload_to="images", 
                              blank=True, 
                              null=True)

    class Meta:
        ordering = ('created',)
