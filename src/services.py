import json
import logging
from typing import Any

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
