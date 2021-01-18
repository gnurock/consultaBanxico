import requests
myToken= 'f796952bfda108d85c0c39bc01497f40a9825ba9b5421033c77b0f9ba4fb783d'

def generate_request(params):
    """
        Funcion para hacer request a la api de banxico
        Dependencias : requests
        Parametros:
            - fecha_i: fecha inicial
            - fecha_f: fecha final
            - seris: numero de serie o series de los catalogos a consultar
        Returns:
            Response: regrea un json obtenido del reponse a la api. 
    """
    
    headers = {'Bmx-Token': myToken}
  

    url_udis="https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos/{fecha_i}/{fecha_f}".format(
        fecha_i=params['fecha_ini'],
        fecha_f=params.get("fecha_fin"),
        series=params.get("serie")
    )
    
   
    response = requests.get(url_udis, headers=headers)    
   
    if response.status_code == 200:
        return response.json()

def get_series(params):
    """
        Funcion para retornar la serie en forma de diccionario
        
    """
    response = generate_request(params)
    if response:
       serie = response.get('bmx')
       return serie.get('series')

    return ""
