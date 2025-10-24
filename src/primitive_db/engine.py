import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table, list_tables, insert, select, update, delete
from .parser import parse_where, parse_set
from prettytable import PrettyTable


COMMANDS = {
     'exit': 'выйти из программы',
     'help': 'справочная информация',
     'create': '<имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу',
     'drop': '<имя_таблицы> - удалить таблицу',
     'list': 'показать список всех таблиц',
     'insert into': '<имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись',
     'select': 'from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.',
     'update': '<имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.',
     'delete': 'from <имя_таблицы> where <столбец> = <значение> - удалить запись.',
     'info': '<имя_таблицы> - вывести информацию о таблице.'
 }

def show_help():
    for cmd, description in COMMANDS.items():
           print(f'{cmd:} - {description}')
           
def print_pretty_table(rows):
    if not rows:
        print("Нет данных для отображения.")
        return

    columns = list(rows[0].keys())

    table = PrettyTable()
    table.field_names = columns

    for row in rows:
        table.add_row([row.get(col, '') for col in columns])

    print(table)            

    
def run():
    
    metadata = load_metadata()
    print('Добро пожаловать в базу данных! Введите help для справки.')
    
    while True:
        try:
            user_input = input('Введите команду: ')
            
            if not user_input:
                continue
            
            args = shlex.split(user_input)
            command = args[0]
            match command:
                case 'create':
                    if len(args) < 3:
                        print('Ошибка: Используйте: create <имя_таблицы> <столбец1:тип> <столбец2:тип> ...')
                        continue
                    
                    table_name = args[1]
                    columns = args[2:]
                    
                    if create_table(metadata, table_name, columns):
                        save_metadata(metadata)
                    else: 
                        print(f'Ошибка при создании таблицы {table_name}')
                    
                case 'drop':
                    if len(args) < 2:
                        print('Ошибка: Используйте: drop <имя_таблицы>')
                        continue
                    
                    table_name = args[1]
                    if drop_table(metadata, table_name):
                        save_metadata(metadata)
                    else:
                        print(f'Ошибка при удалении таблицы {table_name}')
                    
                case 'list':
                    tables = list_tables(metadata)
                    
                    if not tables:
                        print('Нет созданных таблиц!')
                        continue
                    print('Список таблиц:')
                    for t in tables:
                        print(t)
                
                case 'insert':
                    if args[0].lower() == 'insert' and args[1].lower() == 'into':
                        table_name = args[2]
                        values_str = user_input.split('values', 1)[1].strip()
                        values_str = values_str.strip("()")
                        values = [v.strip().strip('"').strip("'") for v in values_str.split(',')]
                        success = insert(metadata, table_name, values)
                        if success:
                            save_metadata(metadata)
                        else:
                            print(f'Ошибка при сохранении записи в таблицу {table_name}!')

                case 'info':
                    if len(args) < 2:
                        print("Ошибка: используйте info <имя_таблицы>")
                        continue

                    table_name = args[1]
                    table = metadata.get(table_name)
                    
                    if not table:
                        print(f"Таблица {table_name} не найдена!")
                        continue

                    columns = table['columns']
                    rows = table.get('rows', [])

                    print(f"Информация о таблице {table_name}:")
                    print("Колонки:")
                    for col_name, col_type in columns.items():
                        print(f" - {col_name}: {col_type}")
                    print(f"Количество строк: {len(rows)}")

                    if rows:
                        print("Примеры записей:")
                        for row in rows[:5]:  # показываем первые 5 записей
                            print(row)
                        
                case 'select':
                    if len(args) < 2:
                        print('Ошибка: используйте select <имя_таблицы> [where <условие>]')
                        continue
                    
                    table_data = args[1]
                    table_data = metadata.get(table_name, {}).get('rows', [])
                    where_clause = None
                    if 'where' in args:
                        where_index = args.index('where')
                        where_str = ' '.join(args[where_index + 1:])
                        where_clause = parse_where(where_str)

                    result = select(table_data, where_clause)
                    if not result:
                        print('Записи не найдены.')    
                    for row in result:
                        print_pretty_table(result)
                    
                case 'update':
                    if len(args) < 4 or 'set' not in args:
                        print('Ошибка: используйте update <таблица> set <столбец=значение,...> [where <условие>]')
                        continue
                    
                    table_name = args[1]
                    table_data = metadata.get(table_name, {}).get('rows', [])
                    
                    set_index = args.index('set')
                    set_str = ' '.join(args[set_index + 1:])
                    
                    where_clause = None
                    if 'where' in args:
                        where_index = args.index('where')
                        set_str = ' '.join(args[set_index + 1:where_index])
                        where_str = ' '.join(args[where_index + 1:])
                        where_clause = parse_where(where_str)

                    set_clause = parse_set(set_str)
                    if not set_clause:
                        print('Ошибка: данные не обновлены')
                    else:    
                        update(table_data, set_clause, where_clause)
                        save_metadata(metadata)
                
                case 'delete':
                    if len(args) < 5 or args[1].lower() != 'from':
                        print("Ошибка: используйте delete from <имя_таблицы> where <условие>")
                        continue

                    table_name = args[2]
                    table = metadata.get(table_name)

                    if not table:
                        print(f"Таблица {table_name} не найдена!")
                        continue

                    if 'where' not in args:
                        print("Ошибка: укажите условие после where")
                        continue

                    where_index = args.index('where')
                    where_clause = ' '.join(args[where_index + 1:])
                    where_dict = parse_where(where_clause)

                    delete(table['rows'], where_dict)
                    save_metadata(metadata)
                      
                case 'exit':
                    print('Выход из программы')
                    break
                    
                case 'help':
                    show_help()
                
                case _:
                    print(f'Неизвестная команда {command}')
                    print("Введите 'help' для списка команд")
                
        except KeyboardInterrupt:
            print("\nВыход из программы...")
            break
        except Exception as e:
            print(f'Прозошла ошибка {e}')
                