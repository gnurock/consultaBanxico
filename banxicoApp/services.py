import requests
myToken= 'f796952bfda108d85c0c39bc01497f40a9825ba9b5421033c77b0f9ba4fb783d'

def generate_request(params):
    headers = {'Bmx-Token': myToken}
  

    url_udis="https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos/{fecha_i}/{fecha_f}".format(
        fecha_i=params['fecha_ini'],
        fecha_f=params.get("fecha_fin"),
        series=params.get("serie")
    )
    
    #headers={'Authorization': 'access_token myToken'})
    # payload = {'datos':fecha_i,fecha_f}
    #url2= "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SP74665,SF61745,SF60634,SF43718,SF43773/datos/2020-01-01/2020-01-08"
    response = requests.get(url_udis, headers=headers)    
    #import pdb; pdb.set_trace()
    if response.status_code == 200:
        return response.json()

def get_series(params):
    response = generate_request(params)
    if response:
       serie = response.get('bmx')
       return serie.get('series')

    return ""
