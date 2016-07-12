import json
import requests

TOKEN_ID = 'bec2016b-638e-4df8-96e3-4434b5c7e05b'
# 37.532889,55.800062 nearby Aeroport metro station
# 37.574452,55.761205 nearby Moscow Zoo
CENTRAL_POINT = '37.532889,55.800062' # nearby Aeroport metro station
SEARCH_AREA_SIZE = '0.017,0.017'
RESTAURANT_NAME = 'KFC'

class Restaurant:
    name = '' # KFC, BK or MD
    address = '' # e.g. Ленингрдаский проспект, 1
    coordinates = '' # e.g. 37.532889,55.800062
    def __init__(self, name, address, coordinates):
        self.name = name
        self.address = address
        self.coordinates = coordinates

# using Yandex Maps Organizations Search API
def getData():
    url = 'https://search-maps.yandex.ru/v1/?results=9999&text={}&ll={}&spn={}&type=biz&lang=ru_RU&apikey={}'.format(RESTAURANT_NAME, CENTRAL_POINT, SEARCH_AREA_SIZE, TOKEN_ID)
    req = requests.get(url)
    d = json.loads(req.text) # json to dict
    number_of_search_results = d['properties']['ResponseMetaData']['SearchResponse']['found']
    restaurants = []

    i = 0
    while True:
        try:
            name = d['features'][i]['properties']['CompanyMetaData']['name']
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
    return restaurants

# using Yandex Maps Static API
def constructMapURL(restaurants):
    s = ''
    for r in restaurants:
        s += r.coordinates + ',round~'
    s = s[:-1] # delete last '~'
    if s == '':
        return 'Sorry, nothing was found'
    return 'https://static-maps.yandex.ru/1.x/?l=map&z=14&ll={}&pt={}'.format(CENTRAL_POINT, s)

restaurants = getData()
print(constructMapURL(restaurants))
