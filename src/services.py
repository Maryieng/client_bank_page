import json

from src.utils import reading_data_from_file
import re


def simple_search(request: str) -> list:
    """ Пользователь передает строку для поиска, возвращается json-ответ со всеми транзакциями,
    содержащими запрос в описании или категории """
    try:
        list_transactions = reading_data_from_file('operations.xls')
        search_results = list_transactions.loc[(list_transactions["Категория"].str.contains(request, case=False)) |
                                          (list_transactions["Описание"].str.contains(request, case=False))]
        search_results_json = search_results.to_json(orient="records", force_ascii=False)
        return json.loads(search_results_json)
    except Exception as e:
            print("An error occurred:", str(e))
            return []
