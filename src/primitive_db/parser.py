
def parse_condition(condition_str: str) -> dict:
    """
    Разбирает простое условие вида:
      "age = 28" -> {"age": 28}
      "name = 'Alice'" -> {"name": "Alice"}
    """
    result = {}
    if not condition_str:
        return result

    parts = [p.strip() for p in condition_str.split(",") if p.strip()]

    for part in parts:
        if "=" not in part:
            raise ValueError(f"Некорректное выражение: {part}")
        key, value = [x.strip() for x in part.split("=", 1)]

        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            value = value[1:-1]
        else:
            try:
                if "." in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  
        result[key] = value
    return result


def parse_where(where_clause: str) -> dict:
    return parse_condition(where_clause)


def parse_set(set_clause: str) -> dict:
    return parse_condition(set_clause)


