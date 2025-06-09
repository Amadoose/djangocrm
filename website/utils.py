# customers/utils.py
import requests, json
from django.conf import settings
from django.contrib.staticfiles import finders


def fetch_country_choices():
    try:
        response = requests.get('https://restcountries.com/v3.1/all')
        countries = sorted(response.json(), key=lambda c: c.get('name', {}).get('common', ''))
        return [(c.get('cca2'), f"{c.get('flag', '')} {c.get('name', {}).get('common')}") for c in countries if c.get('cca2')]
    except Exception:
        return [('MX', '🇲🇽 Mexico'), ('US', '🇺🇸 United States'), ('CA', '🇨🇦 Canada')]
    

def get_dial_code_by_country(iso_code):
    path = finders.find('js/country_dial_codes.json')
    if not path:
        return '+'
    with open(path, 'r', encoding='utf-8') as f:
        countries = json.load(f)
        for c in countries:
            if c['iso'] == iso_code:
                return c['dialCode']
    return '+'