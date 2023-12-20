import json
import logging
import datetime
import math
from pprint import pprint

import pandas as pd
from typing import Any
import re
from src.utils import reading_data_from_file

logger = logging.getLogger('__func_services__')
file_handler_masks = logging.FileHandler('services_loger.log', 'w', encoding='utf-8')
file_formatter_masks = logging.Formatter('%(asctime)s %(module)s %(levelname)s %(message)s')
file_handler_masks.setFormatter(file_formatter_masks)
logger.addHandler(file_handler_masks)
logger.setLevel(logging.INFO)


def simple_search(request: str) -> Any:
    """ Пользователь передает строку для поиска, возвращается json-ответ со всеми транзакциями,
    содержащими запрос в описании или категории """
    try:
        list_transactions = reading_data_from_file('operations.xls')
        search_results = list_transactions.loc[(list_transactions["Категория"].str.contains(request, case=False))
                                               | (list_transactions["Описание"].str.contains(request, case=False))]
        search_results_json = search_results.to_json(orient="records", force_ascii=False)
        logger.info('Успешно. simple_search()')
        return json.loads(search_results_json)
    except Exception as e:
        logger.error(f'Произошла ошибка: {str(e)} в функции simple_search()')
        return []


def search_phone_numbers() -> Any:
    """ Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера """
    try:
        list_transactions = reading_data_from_file('operations.xls')
        pattern = re.compile(r'\d{3}-\d{2}-\d{2}')
        list_from_mobile = list_transactions[list_transactions['Описание'].str.contains(pattern, regex=True)]
        search_results_json = list_from_mobile.to_json(orient="records", force_ascii=False)
        logger.info('Успешно. simple_search()')
        return json.loads(search_results_json)
    except Exception as e:
            logger.error(f'Произошла ошибка: {str(e)} в функции simple_search()')
            return 'Не найдено'


def search_transfers_to_individuals() -> Any:
    """ Функция возвращает JSON со всеми транзакциями-переводы физ. лицам """
    try:
        list_transactions = reading_data_from_file('operations.xls')
        pattern = re.compile(r"\b[А-Я][а-я]+\s[А-Я]\.")
        list_from_mobile = list_transactions[list_transactions['Описание'].str.contains(pattern, regex=True)]
        search_results_json = list_from_mobile.to_json(orient="records", force_ascii=False)
        logger.info('Успешно. simple_search()')
        return json.loads(search_results_json)
    except Exception as e:
        logger.error(f'Произошла ошибка: {str(e)} в функции simple_search()')
        return 'Не найдено'


def invest_copilka(month: str, transactions: pd.DataFrame, limit: int) -> float:
    """ Принимает данные операций , дату и лимит округления. исходя из параметров возвращает сумму возможного
     накопления """
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    extracted_data = transactions[(transactions['Дата операции'].dt.month == month) &
                                  (transactions['Дата операции'].dt.year == 2021)]
    extracted_data.to_csv('output.csv', index=False)
    copilka = 0
    for pos in extracted_data['Сумма операции с округлением']:
        pos = abs(int(pos['Сумма операции с округлением']))
        if limit == 50:
            rounded_amount = math.ceil(pos / 100) * 100
            difference = rounded_amount - pos - limit
            if difference <= 0:
                round_amount = rounded_amount - pos
            else:
                round_amount = difference
        elif limit == 10 or limit == 100:
            round_amount = math.ceil(pos / limit) * limit - pos
        else:
            round_amount = 0
        copilka += round_amount
    return copilka

pprint(invest_copilka(5, reading_data_from_file('operations.xls'), 50))