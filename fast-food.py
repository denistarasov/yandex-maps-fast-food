import json
import requests

TOKEN_ID = 'bec2016b-638e-4df8-96e3-4434b5c7e05b'
CENTRAL_POINT = '37.532889,55.800062' # nearby Aeroport metro station
SEARCH_AREA_SIZE = '0.017,0.017'
RESTAURANT_NAME = 'KFC'

class Restaurant:
    name = '' # KFC, BK or MD
    address = '' # e.g. Ленингрдаский проспект, 1
    coordinates = '' # e.g. 37.532889,55.800062

# add other restaurants except KFC (e.g. BK & McDonalds)
def getData():
    req = requests.get('https://search-maps.yandex.ru/v1/?text={}&ll={}&spn={}&type=biz&lang=ru_RU&apikey={}'.format(RESTAURANT_NAME, CENTRAL_POINT, SEARCH_AREA_SIZE, TOKEN_ID))
    d = json.loads(req.text) # json to dict
    number_of_search_results = d['properties']['ResponseMetaData']['SearchResponse']['found']
    restaurants = []
    for i in range(0, number_of_search_results):
        rest = Restaurant()
        rest.name = d['features'][i]['properties']['CompanyMetaData']['Chains'][0]['name']
        rest.address = d['features'][i]['properties']['CompanyMetaData']['address']
        rest.coordinates = d['features'][i]['geometry']['coordinates']
        restaurants.append(rest)
    return restaurants 

# using Yandex Maps Static API
def constructMapURL(restaurants):
    s = ''
    for r in restaurants:
        s += str(r.coordinates[0]) + ',' + str(r.coordinates[1]) + ',round~'
    s = s[:-1] # delete last '~'
    return 'https://static-maps.yandex.ru/1.x/?l=map&pt={}'.format(s)

restaurants = getData()
# little debugging
# for i in restaurants:
#    print(i.name + ', ' + i.address + ', ' + str(i.coordinates[0]) + str(i.coordinates[1]) + '\n')
print(constructMapURL(restaurants))
