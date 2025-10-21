import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table, list_tables


COMMANDS = {
     'exit': 'выйти из программы',
     'help': 'справочная информация',
     'create': '<имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу',
     'drop': '<имя_таблицы> - удалить таблицу',
     'list': 'показать список всех таблиц'
 }

def show_help():
    for cmd, description in COMMANDS.items():
           print(f'{cmd:} - {description}') 

    
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
                