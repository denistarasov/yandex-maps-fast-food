import requests

TOKEN_ID = 'bec2016b-638e-4df8-96e3-4434b5c7e05b'
CENTRAL_POINT = '37.532889,55.800062' #almost Aeroport metro station
SEARCH_AREA_SIZE = '0.017,0.017'
RESTAURANT_NAME = 'KFC'

class Restaurant:
    name = '' # KFC, BK or MD
    address = ''

# add other restaurants except KFC (e.g. BK & MacDonalds)
def getData():
    req = requests.get('https://search-maps.yandex.ru/v1/?text={}&ll={}&spn={}&type=biz&lang=ru_RU&apikey={}'.format(RESTAURANT_NAME, CENTRAL_POINT, SEARCH_AREA_SIZE, TOKEN_ID))
    print(req.json())
getData()
