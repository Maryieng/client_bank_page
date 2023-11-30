from src.views import displaying_statistics_on_cards


def test_displaying_statistics_on_cards():
    json_data = []
    result = displaying_statistics_on_cards(json_data)
    assert result == {'Приветствие': 'Добрый день!', 'Карты': [
        {'Последние цифры': '*7197', 'Всего потрачено': 0, 'Кэшбэк': 0},
        {'Последние цифры': '*4556', 'Всего потрачено': 0, 'Кэшбэк': 0}], 'Топ-транзакции':
        [], 'Курсы валют': [{'Валюта': 'USD', 'Цена': 88.66},
                            {'Валюта': 'EUR', 'Цена': 96.87}], 'Цены на акции':
        [{'Акция': 'AAPL', 'Цена': 189.37}, {'Акция': 'AMZN', 'Цена': 146.32},
         {'Акция': 'GOOGL', 'Цена': 134.99}, {'Акция': 'MSFT', 'Цена': 378.85}, {'Акция': 'TSLA', 'Цена': 244.14}]}

    assert displaying_statistics_on_cards('json') == {'Ошибка': "Произошла ошибка:"
                                                                " string indices must be integers, not 'str'"}
