import requests
import json
import csv
from datetime import datetime



latitude = -3.1019
longitude = -60.025


url = 'https://api.open-meteo.com/v1/forecast'

parametros = {
    "latitude": latitude,
    "longitude": longitude,
    "current":["temperature_2m", "relative_humidity_2m", "soil_moisture_1_to_3cm", "uv_index_clear_sky"],
    "temporal_resolution": "hourly_6"
}

response = requests.get(url, params=parametros)

if response.status_code == 200:
    dados = response.json()
    print("### clima atual ###")
    print("temperatura", dados['current']['temperature_2m']," C")
    print("umidade", dados['current']['relative_humidity_2m']," %")
    print("umidade do solo", dados['current']['soil_moisture_1_to_3cm'] * 100, "%")
    print("velocidade do vento", dados['current']['uv_index_clear_sky'], "uv")
else:
    print("erro ao conectar a api")