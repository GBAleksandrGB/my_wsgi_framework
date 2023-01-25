from datetime import date
from json import loads

import requests


def date_front(environ, request):
    request['cur_date'] = date.today().strftime('%d.%m.%Y')


def location_front(environ, request):
    ip_address = environ.get('REMOTE_ADDR', '')
    if ip_address:
        response = requests.get('https://geolocation-db.com/jsonp/' + ip_address)
        text = response.content.decode()
        text = text.split("(")[1].strip(")")
        request['location'] = loads(text)


fronts = [date_front, location_front]
