from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    short_description = models.TextField(blank=True, verbose_name="Краткое описание")
    long_description = HTMLField(blank=True, verbose_name="Полное описание")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")

    def __str__(self):
        return self.title


class Image(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Имя фотографии"
    )
    img = models.ImageField(upload_to='images/', verbose_name="Фотография")
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Локация"
    )
    order = models.PositiveIntegerField(default=0, db_index=True, verbose_name="Порядковый номер")

    class Meta:

        ordering = ['order']

    def __str__(self):
        return f"{self.place.title}"