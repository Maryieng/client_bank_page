from collections import OrderedDict
from src.utils import greetings, data_currency_and_share_request


def displaying_statistics_on_cards(json_data: list) -> dict:
    """ возвращает json-ответ в формате: 1. Приветствие 2. По каждой карте: Последние 4 цифры карты,
    Общая сумма расходов, Кэшбэк, Топ-5 транзакции по сумме платежа, Курс валют, Стоимость акций из S&P 500 """
    try:
        list_by_first_card = [dict_data for dict_data in json_data if dict_data['Номер карты'] == '*7197']
        list_by_second_card = [dict_data for dict_data in json_data if dict_data['Номер карты'] == '*4556']
        final_list_for_the_user = OrderedDict()
        final_list_for_the_user["Приветствие"] = greetings()
        final_list_for_the_user["Карты"] = [{
            "Последние цифры": '*7197',
            "Всего потрачено": round(sum([expenses['Сумма платежа'] for expenses in list_by_first_card
                                          if expenses['Сумма платежа'] < 0])),
            "Кэшбэк": sum([expenses.get('Бонусы (включая кэшбэк)') for expenses in list_by_first_card
                           if expenses.get('Бонусы (включая кэшбэк)') is not None])},
            {"Последние цифры": '*4556',
            "Всего потрачено": round(sum([expenses['Сумма платежа'] for expenses in list_by_second_card
                                          if expenses['Сумма платежа'] < 0])),
            "Кэшбэк": round(sum([expenses.get('Бонусы (включая кэшбэк)') for expenses in list_by_second_card
                                 if expenses.get('Бонусы (включая кэшбэк)') is not None]))}]

        sorted_list_by_amount = sorted(json_data,
                                       key=lambda d: d['Сумма операции с округлением'], reverse=True)

        final_list_for_the_user["Топ-транзакции"] = [{"Дата": item['Дата платежа'],
                                    "Сумма": item['Сумма операции'],
                                    "Категория": item['Категория'],
                                    "Описание": item['Описание']} for item in sorted_list_by_amount[:5]]
        currencies, stocks = data_currency_and_share_request('user_settings.json')
        final_list_for_the_user["Курсы валют"] = [*currencies]
        final_list_for_the_user["Цены на акции"] = [*stocks]
        final_list_for_the_user_dict = dict(final_list_for_the_user)
        return final_list_for_the_user_dict
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        return {"Ошибка": error_message}
