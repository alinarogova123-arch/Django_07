from io import BytesIO
from pathlib import Path

import requests
from django.core.management.base import BaseCommand
from django.core.files import File

from places.models import Place, Image


def add_image_to_place(image_urls, place):
	for image_url in image_urls:
		response = requests.get(image_url)
		response.raise_for_status()
		image = BytesIO(response.content)
		image_file = File(image, name=Path(image_url).name)
		img, created = Image.objects.get_or_create(
			name=Path(image_url).name,
			place=place,
			defaults={
        		'img': image_file
    		}
		)


class Command(BaseCommand):
	help = "Добавляет запись в модель Place"


	def add_arguments(self, parser):
		parser.add_argument("url", type=str, help="url JSON файла")


	def handle(self, *args, **options):
		url = options["url"]
		response = requests.get(url)
		response.raise_for_status()
		serialize_place = response.json()
		image_urls = serialize_place.get("imgs")
		place, created = Place.objects.get_or_create(
			title=serialize_place.get("title"),
    		short_description=serialize_place.get("description_short"),
    		long_description=serialize_place.get("description_long"),
    		lat=serialize_place.get("coordinates").get("lat"),
    		lon=serialize_place.get("coordinates").get("lng"),
    	)
		add_image_to_place(image_urls, place)