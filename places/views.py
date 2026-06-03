from django.shortcuts import render
from .models import Place, Image

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