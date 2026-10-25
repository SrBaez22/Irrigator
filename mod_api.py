import requests
import csv

latitude = -3.1019
longitude = -60.025

url = "https://archive-api.open-meteo.com/v1/archive"

parametros = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2023-01-01",
    "end_date": "2025-12-31",
    "hourly": ",".join([
        "temperature_2m",
        "relative_humidity_2m",
        "soil_moisture_0_to_7cm",
        "shortwave_radiation",
    ]),
    "timezone": "America/Manaus",
}

try:
    response = requests.get(url, params=parametros, timeout=60)
    response.raise_for_status()
    dados = response.json()["hourly"]

    tempo = dados["time"]
    temp = dados["temperature_2m"]
    umid_ar = dados["relative_humidity_2m"]
    umid_solo = dados["soil_moisture_0_to_7cm"]
    radiacao = dados["shortwave_radiation"]

    with open("dados_manaus_horarios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "air_temperature_c", "relative_humidity_pct",
                    "soil_moisture_pct", "solar_radiation_wm2"])
        for i in range(len(tempo)):
            solo = umid_solo[i] * 100 if umid_solo[i] is not None else None
            w.writerow([tempo[i], temp[i], umid_ar[i], solo, radiacao[i]])

    print(f"{len(tempo)} linhas salvas em dados_manaus_horarios.csv")
    print("Primeira linha:", tempo[0], temp[0], "°C |", umid_ar[0], "% |",
          umid_solo[0] * 100 if umid_solo[0] is not None else None, "% |",
          radiacao[0], "W/m²")

except requests.exceptions.HTTPError as erro:
    print(f"Erro HTTP: {erro}\nDetalhe da API: {response.text}")
except requests.exceptions.RequestException as erro:
    print(f"Erro ao chamar a API: {erro}")
except (ValueError, KeyError, TypeError) as erro:
    print(f"Erro ao interpretar a resposta da API: {erro}")