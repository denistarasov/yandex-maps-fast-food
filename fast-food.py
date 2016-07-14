import json
import requests

TOKEN_ID = 'bec2016b-638e-4df8-96e3-4434b5c7e05b'
CENTRAL_POINT = '37.620393,55.753960' # Moscow central point
SEARCH_AREA_SIZE = '0.017,0.017'

class Restaurant:
    name = '' # KFC, BK or MD
    address = '' # e.g. Ленинградский проспект, 1
    coordinates = '' # e.g. 37.532889,55.800062
    def __init__(self, name, address, coordinates):
        self.name = name
        self.address = address
        self.coordinates = coordinates

# Using Yandex Maps Geocoder API
# The function converts address string to coordinates
def addressToPoint(address):
    url = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode=Москва,+{}'.format(address)
    req = requests.get(url)
    d = json.loads(req.text)
    coordinates = d['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'] # e.g. 37.611347 55.760241
    return coordinates.replace(" ", ",") # '37.611347 55.760241' -> '37.611347,55.760241'
        
# Using Yandex Maps Organizations Search API
# The function receives brand name and returns a list
# containing all found restaurants in the nearest area
def getData(brand_name):
    url = 'https://search-maps.yandex.ru/v1/?results=9999&text={}&ll={}&spn={}&type=biz&lang=ru_RU&apikey={}'.format(brand_name, CENTRAL_POINT, SEARCH_AREA_SIZE, TOKEN_ID)
    req = requests.get(url)
    d = json.loads(req.text) # json to dict
    number_of_search_results = d['properties']['ResponseMetaData']['SearchResponse']['found']
    global restaurants

    i = 0
    while i < 10:
        try:
            name = brand_name # d['features'][i]['properties']['CompanyMetaData']['name']
            address = d['features'][i]['properties']['CompanyMetaData']['address']
            coordinates_list = d['features'][i]['geometry']['coordinates']
            coordinates = str(coordinates_list[0]) + ',' + str(coordinates_list[1])
            restaurants.append(Restaurant(name, address, coordinates))
            i += 1
        except IndexError:
            break
        except KeyError:
            i += 1
            continue

# Using Yandex Maps Static API
# The function returns a link to a map which show
# the closest restaurants
# that were found with getData() function
def constructMapURL(restaurants):
    s = ''
    for r in restaurants:
        global brand_names
        if r.name == brand_names[0]:
            point_color = 'yw'
        elif r.name == brand_names[1]:
            point_color = 'rd'
        elif r.name == brand_names[2]:
            point_color = '2rd'
        else:
            point_color = 'gr'
        s += '{},pm{}m~'.format(r.coordinates, point_color)
    s = s[:-1] # delete last '~'
    if s == '':
        return 'Sorry, nothing was found'
    return 'https://static-maps.yandex.ru/1.x/?l=map&z=14&ll={}&pt={}'.format(CENTRAL_POINT, s)

####################

print('''This program searches the nearest fast-food restaurants to a certain location.
Enter your location. E.g. ['красная площадь'].
If address is not found, then the central point will be ['красная площадь']''')
CENTRAL_POINT = addressToPoint(input())
restaurants = []
brand_names = ['макдоналдс', 'kfc', 'бургер кинг']
getData(brand_names[0])
getData(brand_names[1])
getData(brand_names[2])
print(constructMapURL(restaurants))
