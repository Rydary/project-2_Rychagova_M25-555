from .parser import parse_where, parse_set

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
               
        
def insert(metadata, table_name, values):
    table = metadata.get(table_name)
    
    if not table:
        print(f'Такой таблицы {table_name} не существует')
        return False
    
    
    columns = table['columns']
    col_names = [col for col in columns if col != 'ID']
    
    if len(values) != len(columns) - 1:
        print(f'В таблице {table_name} - {len(columns) - 1} столбцов (без учета ID) !')
    

    record = {}
    for name, val in zip(col_names, values):
        expected_type = columns[name]
        try:
            if expected_type == 'int':
                val = int(val)
            elif expected_type == 'bool':
                val = val.lower() in ('true', '1', 'yes')
            elif expected_type == 'str':
                val = str(val)
        except Exception:
            print(f'Ошибка! Столбец {name} должен быть типа {expected_type}.')
            return False
        record[name] = val
    
    existing_ids = [r['ID'] for r in table.get('rows', [])]
    new_id = max(existing_ids, default=0) + 1
    record['ID'] = new_id

    table.setdefault('rows', []).append(record)
    print(f'Добавлена запись с ID={new_id}')
    return True
    
 
def select(table_data, where_clause=None):

    if not table_data:
        print('Таблица пуста!')
        
    if not where_clause:
        return table_data
    
    filtered_data = []
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break
        if match:
            filtered_data.append(row)        
    
    return filtered_data
        

def update(table_data, set_clause, where_clause):
    if not table_data:
        print('Таблица пуста!')
        return []
    
    if not where_clause:
        print('уточните условие поиска!')
        return table_data
        
    if not set_clause:
        print('Уточните значения для замены!')
        return table_data
    
    if isinstance(where_clause, str):
        where_clause = parse_where(where_clause)
    if isinstance(set_clause, str):
        set_clause = parse_set(set_clause) 
        
    updated_count = 0
    
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break
        if match:
           for set_key, set_value in set_clause.items():
               row[set_key] = set_value
               updated_count += 1
            
    if updated_count == 0:
        print('Значения по заданным условиям не найдены!')
    else:
        print(f'Обновлено записей: {updated_count}')
    
    return table_data      
          
def delete(table_data, where_clause):
    if not table_data:
        print('Таблица пуста!')
        return []
    
    if not where_clause:
        print('Задайте условия для удаления строк таблицы!')
        return table_data
    
    if isinstance(where_clause, str):
        where_clause = parse_where(where_clause)
        
    
    original_len = len(table_data)
    
    table_data[:] = [
        row for row in table_data
        if not all(row.get(k) == v for k, v in where_clause.items())
    ]
    
    deleted_count = original_len - len(table_data)
                
    if deleted_count == 0:
        print('Данные для удаления не найдены!')
    else:
        print(f'Удалено строк: {deleted_count}')
        
    return table_data