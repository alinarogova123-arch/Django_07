from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField()
    description_long = HTMLField()
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.title


class Image(models.Model):
    img = models.ImageField(upload_to='images/')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="images")
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:

        ordering = ['order']

    def __str__(self):
        return f"{self.order} {self.place.title}"