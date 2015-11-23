from django.shortcuts import render
from .models import Location

# Create your views here.
def index(request):
    return render(request, 'locations/index.html', {})

def get_distance(initial, final):
    '''
    :param initial (list: [latitide, longitude]):
    :param final (list: [latitide, longitude]):
    :return: distance in meters
    '''
    import math

    R = 6371000
    phi1 = math.radians(float(initial[0]))
    phi2 = math.radians(float(final[0]))
    dphi = math.radians(float(final[0]) - float(initial[0]))
    dl = math.radians(float(final[1]) - float(initial[1]))
    a = (math.sin(dphi/2)**2) + (math.cos(phi1) * math.cos(phi2) * math.sin(dl/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def show(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    locations = Location.objects.filter()
    places = []
    for i in locations:
        if abs(get_distance([latitude, longitude], [i.latitude, i.longitude])) <= 150:
            places.append([i.latitude, i.longitude, i.weight])
    places.sort(key= lambda place: -place[2])
    if len(places) > 10:
        places = places[:10]
    print(places)
    ct = {
        'show': True,
        'latitude': latitude,
        'longitude': longitude,
        'places': places,
    }
    return render(request, 'locations/index.html', ct)
