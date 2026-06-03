from django.shortcuts import render
from .models import Place, Image
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse

# Create your views here.


def serialize_place(place):
    return {
      'type': 'Feature',
      'geometry': {
        'type': 'Point',
        'coordinates': [place.lon, place.lat]
      },
      'properties': {
        'title': place.title,
        'placeId': place.id,
        'detailsUrl': './static/places/moscow_legends.json'
      }
    }


def index(request):
	places = Place.objects.all()
	context = {
		'places': {
			'type': 'FeatureCollection',
      		'features': [serialize_place(place) for place in places],
		},
	}

	return render(request, 'index.html', context)


def places_detail(request, place_id):
	place = get_object_or_404(Place, id=place_id)
	images = []
	for image in place.images.all():
		images.append(image.img.url)
	response_data = {
		'title': place.title,
		'imgs': images,
		'description_short': place.description_short,
		'description_long': place.description_long,
		'coordinates': {
			'lat': place.lat,
			'lng': place.lon,
		}
	}
	return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})
