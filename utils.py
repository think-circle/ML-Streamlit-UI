from geopy.geocoders import Nominatim
from geopy.distance import geodesic as gd

def get_coordinates(suburb,city):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(f"{suburb},{city},Australia")
    return getLoc.latitude,getLoc.longitude

def calc_distance(suburb,city):
    lat0,long0 = get_coordinates(city,city)
    lat1,long1 = get_coordinates(suburb,city)
    dist = round(gd((lat0, long0), (lat1, long1)).km,2)
    print(dist)
    return dist
