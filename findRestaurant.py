import httplib2
import requests
import json
# Imports for other languages support like japanese
import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_ID = \
    'ETVHV2AJRFCI5XTR5FLNJLMBYEV3JWOWFLCMORIHHMVNGBOT'
foursquare_client_SECRET = \
    '2ITEKOZHVDC1DWN1YFVSMQF0PQOFKG1V0LFVO2HB0EKECALT'
google_api_key = 'AIzaSyCm-wT32GY1obGdC1__cs7uOUdD9ap7xNI'


def getGeocodeLocation(inputString):
    # Replace all "," for no space "", and space " " for "+" sign
    locationString = inputString.replace(" ", "+").replace(",", "")
    url = (
            'https://maps.googleapis.com/maps/api/geocode/json'
            '?address=%s&key=%s' % (
                locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print(result.keys())
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return latitude, longitude


def foursquareSearch(mealtype, glocation):
    coordenates = ''
    for count, element in enumerate(glocation, start=1):
        if count == 2:
            coordenates = coordenates + str(element)
            break
        coordenates = coordenates + str(element) + ', '
    # ########Restaurant name and address##############
    url = 'https://api.foursquare.com/v2/venues/search'
    params = dict(
        client_id=foursquare_client_ID,
        client_secret
        =foursquare_client_SECRET,
        v='20180323',
        intent='browse',
        ll=coordenates,
        radius=250,
        query=mealtype,
        limit=10
    )
    resp = requests.get(url=url, params=params)
    if resp.status_code == 429:
        return quotaExceeded()
    restaurant = json.loads(resp.text)
    # For each object into restaurants retrieve menu and picture
    for x in restaurant['response']['venues']:
        url = 'https://api.foursquare.com/v2/venues/%s/menu' % x['id']
        params = dict(
            client_id=foursquare_client_ID,
            client_secret
            =foursquare_client_SECRET,
            v='20180323')
        resp = requests.get(url=url, params=params)
        if resp.status_code != 200:
            x['rmenu'] = 'Not Available'
            url = 'https://api.foursquare.com/v2/venues/%s/photos' % x[
                'id']
            params = dict(client_id=foursquare_client_ID,
                          client_secret
                          =foursquare_client_SECRET,
                          v='20180323', limit=1, offset=100)
            resp = requests.get(url=url, params=params)
            if resp.status_code != 200:
                x['rphoto'] = 'Not Available'
            continue
        rmenu = json.loads(resp.text)
        x['rmenu'] = rmenu['response']['menu']
        url = 'https://api.foursquare.com/v2/venues/%s/photos' % x['id']
        params = dict(client_id=foursquare_client_ID,
                      client_secret
                      =foursquare_client_SECRET,
                      v='20180323', limit=1, offset=100)
        resp = requests.get(url=url, params=params)
        rphoto = json.loads(resp.text)
        x['rphoto'] = rphoto['response']['photos']['items']
    return restaurant


def findRestaurant(mealType, location):
    geoloc = getGeocodeLocation(location)
    jsonresponse = foursquareSearch(mealType, geoloc)
    print jsonresponse
    return jsonresponse


def quotaExceeded():
    return None
