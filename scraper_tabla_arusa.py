import requests
from bs4 import BeautifulSoup
import json

url = "https://arusa.cl/es/tournament/1304838/ranking/3595238"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tabla = soup.select_one("table.tablestyle-014f")

data = []
filas = tabla.select("tbody tr")

for fila in filas:
    columnas = fila.select("td")
    if not columnas:
        continue

    nombre = columnas[2].get_text(strip=True)
    fila_data = {
        "posicion": columnas[1].get_text(strip=True),
        "nombre": nombre,
        "puntos": columnas[3].get_text(strip=True),
        "pj": columnas[4].get_text(strip=True),
        "pg": columnas[5].get_text(strip=True),
        "pe": columnas[6].get_text(strip=True),
        "pp": columnas[7].get_text(strip=True),
        "gf": columnas[8].get_text(strip=True),
        "gc": columnas[9].get_text(strip=True),
        "dif": columnas[10].get_text(strip=True),
        "resaltado": "Tabancura" in nombre
    }
    data.append(fila_data)

with open("tabla_arusa.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
