# customers/utils.py
import requests


def fetch_country_choices():
    try:
        response = requests.get('https://restcountries.com/v3.1/all')
        countries = sorted(response.json(), key=lambda c: c.get('name', {}).get('common', ''))
        return [(c.get('cca2'), f"{c.get('flag', '')} {c.get('name', {}).get('common')}") for c in countries if c.get('cca2')]
    except Exception:
        return [('MX', '🇲🇽 Mexico'), ('US', '🇺🇸 United States'), ('CA', '🇨🇦 Canada')]
    
