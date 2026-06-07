from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.urls import reverse

from .models import Place, Image


def get_features(place):
    return {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [place.lon, place.lat]
        },
        'properties': {
            'title': place.title,
            'placeId': place.id,
            'detailsUrl': reverse('places', args=[place.id])
        }
    }


def index(request):
    places = Place.objects.all()
    context = {
        'places': {
            'type': 'FeatureCollection',
                'features': [get_features(place) for place in places],
        },
    }

    return render(request, 'index.html', context)


def places_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images = [image.img.url for image in place.images.all()]
    serialize_place = {
        'title': place.title,
        'imgs': images,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lon,
        }
    }
    return JsonResponse(serialize_place, safe=False, json_dumps_params={'ensure_ascii': False})
