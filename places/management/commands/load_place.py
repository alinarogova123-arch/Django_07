from io import BytesIO
from pathlib import Path

import requests
from django.core.management.base import BaseCommand
from django.core.files import File

from places.models import Place, Image


def add_image_to_place(image_urls, place):
	for image_url in image_urls:
		response = requests.get(image_url)
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
		title = response.json().get("title")
		image_urls = response.json().get("imgs")
		place, created = Place.objects.get_or_create(
			title=response.json().get("title"),
    		short_description=response.json().get("description_short"),
    		long_description=response.json().get("description_long"),
    		lat=response.json().get("coordinates").get("lat"),
    		lon=response.json().get("coordinates").get("lng"),
    	)
		add_image_to_place(image_urls, place)