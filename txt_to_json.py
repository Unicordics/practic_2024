import json


def txt_to_json(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        result = {line.strip().replace('"', '').replace("'", ""): {} for line in lines}

        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)

        print(f"Данные успешно записаны в файл {output_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


input_file_path = 'addresses_204002000000_code.txt'
output_file_path = 'coordinates.json'

txt_to_json(input_file_path, output_file_path)
