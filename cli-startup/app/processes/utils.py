

def nullOrValue(value) -> str:
    """
        Функция для создания SQL-параметров при генерации таблиц
    """
    return "null" if not value else str(f"'{value}'")


def NOV(value) -> str :
    """
        Экономия места!
    """
    return nullOrValue(value)