import aiohttp
import asyncio
import json

API_KEY = '9ace5782-2b50-4543-bad8-4e48fffdda0a'
# 5c6da693-0068-4b31-af79-801eab7e1154 18.07+ 13k+ reqs
# 19c4feb8-e332-4c2a-92d3-f02484cb13fa 18k
# 9ace5782-2b50-4543-bad8-4e48fffdda0a gg
# 15642592-27cb-4f51-a65d-3722daf1ef26


async def fetch_coordinates(session, address):
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'
    try:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            if data['response']['GeoObjectCollection']['featureMember']:
                geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                pos = geo_object['Point']['pos'].split()
                lat, lon = float(pos[1]), float(pos[0])
                print(address)
                formatted_address = geo_object['metaDataProperty']['GeocoderMetaData']['text']
                return address, {'lat': lat, 'lon': lon, 'formatted_address': formatted_address}
            else:
                print(f"Not found {address}")
                return address, {'not_found': 1}
    except Exception as e:
        print(f"error {address}: {e}")
        return address, {'error': 'error'}


async def main(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        addresses = json.load(file)
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for address in addresses:
                if not addresses[address] or 'error' in addresses[address]:
                    task = fetch_coordinates(session, address)
                    tasks.append(task)
                if len(tasks) == 100:
                    batch_results = await asyncio.gather(*tasks)
                    for addr, result in batch_results:
                        if result:
                            addresses[addr] = result
                    tasks = []

                    with open(input_file, 'w', encoding='utf-8') as file:
                        json.dump(addresses, file, ensure_ascii=False, indent=4)
                    #await asyncio.sleep(100)

            if tasks:
                batch_results = await asyncio.gather(*tasks)
                for addr, result in batch_results:
                    if result:
                        addresses[addr] = result
    except Exception as e:
        print(e)
    finally:
        with open(input_file, 'w', encoding='utf-8') as file:
            json.dump(addresses, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    input_file_path = 'coordinates.json'
    asyncio.run(main(input_file_path))
