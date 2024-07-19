import pandas as pd
import json


with open('final_cords.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


rows = []
not_f = []
for key, value in data.items():
    if 'not_found' in value:
        not_f.append(key)
    lat = value.get("lat", None)
    lon = value.get("lon", None)
    if lat and lon:
        lat = str(lat).replace(',', '.')
        lon = str(lon).replace(',', '.')
    row = {
        "исходный адрес": key,
        "широта": lat,
        "долгота": lon,
        "адрес яндекса": value.get('formatted_address', None)
    }
    rows.append(row)

#[print(x) for x in not_f]

df = pd.DataFrame(rows)
file_path = 'addresses_coordinates.xlsx'
df.to_excel(file_path, index=False)
