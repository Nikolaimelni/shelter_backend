from flask import Blueprint, jsonify, request
import requests
from flask import current_app
import googlemaps
from ..utils import get_keywords

shelter_routes = Blueprint('shelter_routes', __name__)


def get_photo_url(photo_reference, max_width=400):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={current_app.config['GOOGLE_MAPS_KEY']}"


@shelter_routes.route('/find_places_in_city', methods=['GET'])
def find_places_in_city():
    gmaps = googlemaps.Client(key=current_app.config['GOOGLE_MAPS_KEY'])

    city = request.args.get('city', type=str)
    radius = request.args.get('radius', default=30000, type=int)
    all_results = []
    geocode_result = gmaps.geocode(city)
    if not geocode_result:
        return jsonify({'error': 'City not found'}), 404
    location = geocode_result[0]['geometry']['location']

    keywords = get_keywords()

    for keyword in keywords:
        result = gmaps.places_nearby(location=location, radius=radius, keyword=keyword)
        for place in result.get('results', []):
            # Добавляем URL изображения, если оно доступно
            if place.get('photos'):
                photo_reference = place['photos'][0]['photo_reference']
                place['photo_url'] = get_photo_url(photo_reference)
            all_results.append(place)
    return jsonify(all_results)

@shelter_routes.route('/find_places_nearby', methods=['GET'])
def find_places_nearby():
    gmaps = googlemaps.Client(key=current_app.config['GOOGLE_MAPS_KEY'])

    latitude = request.args.get('lat', type=float)
    longitude = request.args.get('lng', type=float)
    radius = request.args.get('radius', default=30000, type=int)

    all_results = []
    keywords = get_keywords()
    for keyword in keywords:
        result = gmaps.places_nearby(location=(latitude, longitude), radius=radius, keyword=keyword)
        for place in result.get('results', []):
            if place.get('photos'):
                photo_reference = place['photos'][0]['photo_reference']
                place['photo_url'] = get_photo_url(photo_reference)
            all_results.append(place)
    return jsonify(all_results)


@shelter_routes.route('/autocomplete', methods=['GET'])
def autocomplete():
    input_text = request.args.get('input', default='', type=str)
    params = {
        'input': input_text,
        'key': current_app.config['GOOGLE_MAPS_KEY'],
    }
    response = requests.get('https://maps.googleapis.com/maps/api/place/autocomplete/json', params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch autocomplete results'}), response.status_code