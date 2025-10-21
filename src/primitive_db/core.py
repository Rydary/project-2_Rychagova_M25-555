def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Таблица {table_name} уже существует')
        return metadata
    
    has_id = any(col.lower().startswith('id:') for col in columns)
    if not has_id:
        columns = ['ID:int'] + columns
        
    allowed_types = ('int', 'str', 'bool')
    parsed_columns = {}
    
    for col in columns:
        try:
            name, dtype = col.split(':')
        except ValueError:
            print(f'Неверный формат столбца {col}')
            return metadata
        
        if dtype not in allowed_types:
            print(f'Ошибка: недопустимый тип данных {dtype}')
            print(f'Допустимые форматы: {', '.join(allowed_types)}')
            return metadata
        
        parsed_columns[name] = dtype
        
    metadata[table_name] = {
        'columns': parsed_columns,
        'rows': []
        }
        
    print(f'Таблица {table_name} успешно создана!')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Таблицы {table_name} не существует!')
        return metadata
    else: 
        metadata.pop(table_name)
        print(f'Таблица {table_name} удалена!')
        return metadata
    
def list_tables(metadata):
        for table_name in metadata.keys():
            return list(metadata.keys())