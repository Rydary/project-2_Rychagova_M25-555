def create_cacher():
    """
    Создаёт кэшер с замыканием.
    Возвращает функцию cache_result(key, value_func), которая хранит результаты по ключу.
    """
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            print(f'[cache] Результат найден для ключа: {key}')
            return cache[key]
        print(f'[cache] Вычисление результата для ключа: {key}')
        result = value_func()
        cache[key] = result
        return result

    return cache_result