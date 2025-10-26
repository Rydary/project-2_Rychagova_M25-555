import time


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print('Ошибка: Файл данных не найден.' 
                  '/Возможно, база данных не инициализирована.')
        except KeyError as e:
            print(f'Ошибка: Таблица или столбец {e} не найден.')
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
        except Exception as e:
            print(f'Произошла непредвиденная ошибка: {e}')
    
    return wrapper


def confirm_action(func):
    def wrapper(*args, **kwargs):
        answer = input('Вы уверены, что хотите выполнить это действие? [y/n]: ').strip().lower()
        if answer == 'y':
            return func(*args, **kwargs)
        else:
            print('Операция отменена пользователем.')
            return None
    return wrapper


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        duration = end - start
        print(f'Функция {func.__name__} выполнилась за {duration} с.')
        return result
    return wrapper      