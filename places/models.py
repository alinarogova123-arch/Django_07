from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField(blank=True)
    long_description = HTMLField(blank=True)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.title


class Image(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    img = models.ImageField(upload_to='images/')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="images")
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:

        ordering = ['order']

    def __str__(self):
        return f"{self.order} {self.place.title}"