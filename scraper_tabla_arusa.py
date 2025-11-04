import requests
from bs4 import BeautifulSoup
import json
import sys

url = "https://arusa.cl/es/tournament/1304838/ranking/3595239"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error al obtener la tabla: {e}")
    sys.exit(1)  # Finaliza con error para que GitHub Actions lo registre

soup = BeautifulSoup(response.text, "html.parser")
tabla = soup.select_one("table.tablestyle-014f")

if not tabla:
    print("No se encontró la tabla en el HTML.")
    sys.exit(1)

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

print("✅ Tabla actualizada correctamente.")
