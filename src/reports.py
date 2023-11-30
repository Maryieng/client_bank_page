from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def write_result_to_file(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename == f"{timestamp}.txt"
            with open(filename, "w", encoding='utf-8') as file:
                file.write(result.to_string(index=False))
            return result
        return wrapper
    return decorator


@write_result_to_file('my_result.txt')
def spending_by_category(operations: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """ Функция принимает на вход: датафрейм с транзакциями, название категории, опциональную дату,
     по умолчанию текущая дата. Функция возвращает операции по заданной категории за последние 3 месяца
     (от переданной даты)."""
    try:
        if date is None:
            date = datetime.now().date()  # type: ignore
        else:
            date = datetime.strptime(date, "%Y-%m-%d").date()  # type: ignore
        three_months_ago = date - timedelta(days=3 * 30)  # type: ignore
        filtered_df = operations.copy()
        filtered_df['Дата платежа'] = pd.to_datetime(filtered_df['Дата платежа'], dayfirst=True)
        filtered_df = filtered_df[(filtered_df['Категория'] == category)
                                  & (filtered_df['Дата платежа'] >= pd.to_datetime(three_months_ago))
                                  & (filtered_df['Дата платежа'] <= pd.to_datetime(date))]
        return filtered_df
    except Exception as e:
        print("Произошла ошибка:", str(e))
        return pd.DataFrame()
