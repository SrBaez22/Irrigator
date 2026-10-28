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
        "soil_moisture_0_to_7cm",
    ]),
    "timezone": "America/Manaus",
}

# Curva de retenção do artigo (Almeida et al., 2024, Eq. 1): theta = A * T^(-B)
A = 0.5483
B = 0.211


def tensao_kpa(theta):
    """Converte umidade volumétrica (m³/m³) em tensão da água no solo (kPa).
    A equação do artigo só é válida de 0 a 100 kPa, então o resultado é limitado a esse intervalo."""
    if theta is None or theta <= 0:
        return None
    t = (A / theta) ** (1 / B)
    return min(max(t, 0), 100)


try:
    response = requests.get(url, params=parametros, timeout=60)
    response.raise_for_status()
    dados = response.json()["hourly"]

    tempo = dados["time"]
    umid_solo = dados["soil_moisture_0_to_7cm"]

    with open("dados_manaus_horarios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp","soil_moisture_pct", "soil_tension_kpa"])
        for i in range(len(tempo)):
            solo = umid_solo[i] * 100 if umid_solo[i] is not None else None
            tensao = tensao_kpa(umid_solo[i])
            w.writerow([tempo[i], round(solo,2), round(tensao, 2) if tensao is not None else None])

    print(f"{len(tempo)} linhas salvas em dados_manaus_horarios.csv")
    primeiro_solo = umid_solo[0] * 100 if umid_solo[0] is not None else None
    primeira_tensao = tensao_kpa(umid_solo[0])
    print("Primeira linha:", tempo[0], primeiro_solo, "% |", primeira_tensao, "kPa")

except requests.exceptions.HTTPError as erro:
    print(f"Erro HTTP: {erro}\nDetalhe da API: {response.text}")
except requests.exceptions.RequestException as erro:
    print(f"Erro ao chamar a API: {erro}")
except (ValueError, KeyError, TypeError) as erro:
    print(f"Erro ao interpretar a resposta da API: {erro}")