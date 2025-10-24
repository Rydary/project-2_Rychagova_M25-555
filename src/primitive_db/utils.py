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
            return filepath
    except Exception:
        print('Ошибка при сохранении данных')


def load_data_table(table_name):
    filepath = f'data_{table_name}.json'
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print('Файл не найден')
        return []
    except json.JSONDecodeError:
        print(f'Файл {filepath} содержит неверный формат данных.')
        return []
        

def save_table_data(table_name, data):
    filepath = f'data_{table_name}.json'
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'Данные таблицы {table_name} успешно сохранены')
    except Exception as e:
        print(f'Ошибка при сохранении данных таблицы {table_name}: {e}') 
        

                