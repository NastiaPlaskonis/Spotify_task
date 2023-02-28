import pycountry
import geopy.geocoders as g
import folium


geolocator = g.Nominatim(user_agent ="http")


def get_country_name(abbr):
    country = pycountry.countries.get(alpha_2=abbr)
    if country is not None:
        return country.name


def geolocate(country_abbr):
    try:
        loc = geolocator.geocode(country_abbr)
        return (loc.latitude, loc.longitude)
    except:
        return None
    

def get_geodata(abbrs):
    data = []
    for item in abbrs:
        country = get_country_name(item)
        if country is None:
            country = item
        loc = geolocate(item)
        if loc is not None:
            data.append((country, *loc))
    return data


def create_map(markets):
    m = folium.Map()
    for country, lat, lon in markets:
        print(country)
        folium.Marker(location=(lat, lon), popup=country).add_to(m)
    return m