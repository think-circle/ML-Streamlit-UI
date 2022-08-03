from geopy.geocoders import Nominatim
from geopy.distance import geodesic as gd

def get_coordinates(suburb):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(f"{suburb},Victoria,Australia")
    return getLoc.latitude,getLoc.longitude

def calc_distance(suburb):
    lat0,long0 = get_coordinates("Melbourne")
    lat1,long1 = get_coordinates(suburb)
    dist = round(gd((lat0, long0), (lat1, long1)).km,2)
    return dist
