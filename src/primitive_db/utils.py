import json

def load_metadata(filepath='metadata.json'):
    try:
        with open(filepath, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print('Файл содержит неверный формат')
        return {}
    
def save_metadata(data, filepath='metadata.json'):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print(f'Данные сохранены в {filepath}')
    except Exception:
        print('Ошибка при сохранении данных')

