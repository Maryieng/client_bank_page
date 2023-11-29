import json
import os
from typing import Any
import yfinance as yf
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime
import datetime
import logging
load_dotenv()

logger = logging.getLogger('__func_utils__')
file_handler_masks = logging.FileHandler('utils_loger.log', 'w', encoding='utf-8')
file_formatter_masks = logging.Formatter('%(asctime)s %(module)s %(levelname)s %(message)s')
file_handler_masks.setFormatter(file_formatter_masks)
logger.addHandler(file_handler_masks)
logger.setLevel(logging.INFO)


def data_currency_and_share_request(filename: str) -> Any:
    """ получает информацию по валютам и акциям и выводит в виде tuple"""
    current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_directory, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = json.load(f)
            logger.info('Успешно. data_currency_and_share_request()')
    except FileNotFoundError:
        logger.error(f'Файл не найден. data_currency_and_share_request()')
        return [], []
    except Exception as e:
        logger.error(f'Ошибка при чтении файла. data_currency_and_share_request()')
        return [], []
    api_key_currency = os.getenv('api_key_openexchangerates')
    exchange_rates = []
    share_prices = []
    try:
        for currency in text['user_currencies']:
            url_currency = f"https://openexchangerates.org/api/latest.json?app_id={api_key_currency}&symbols={currency},RUB"
            data_currency = requests.get(url_currency).json()
            rates_currency = data_currency["rates"]
            exchange_rate = 1 / rates_currency[currency] * rates_currency['RUB']
            exchange_rates.append({"Валюта": currency, "Цена": exchange_rate})
        for stocks in text['user_stocks']:
            symbol = yf.Ticker(stocks)
            stock_info = symbol.info
            if "currentPrice" in stock_info:
                current_price = stock_info["currentPrice"]
                share_prices.append({"Акция": stocks, "Цена": current_price})
        logger.info('Успешно. data_currency_and_share_request()')
        return exchange_rates, share_prices
    except requests.exceptions.RequestException as e:
        logger.error(f"Произошла ошибка при выполнении запроса API: {e}")
        return [], []
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return [], []


def greetings() -> str:
    """ Приветствие берущее за основу текущее время """
    opts = {"hey": ('Доброе утро!', 'Добрый день!', 'Добрый вечер!', 'Доброй ночи!')}
    now = datetime.datetime.now()
    if now.hour > 4 and now.hour <= 12:
        greet = opts["hey"][0]
    elif now.hour > 12 and now.hour <= 16:
        greet = opts["hey"][1]
    elif now.hour > 16 and now.hour <= 24:
        greet = opts["hey"][2]
    elif now.hour >= 0 and now.hour <= 4:
        greet = opts["hey"][3]
    logger.info("Успешно. greetings()")
    return greet


def reading_data_from_file(filename: str) -> pd.DataFrame:
    """ Чтение данных из файла .xls """
    try:
        current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_directory, 'data', filename)
        logger.info('Успешно reading_data_from_file()')
        return pd.read_excel(file_path, na_values=["NA", "N/A", "missing"])
    except FileNotFoundError:
        logger.error("Файл не найден.")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Произошла ошибка при чтении файла: {e}")
        return pd.DataFrame()


def outputting_statistics_based_on_data(user_date: str) -> pd.DataFrame:
    """ на вход дается дата начала и конца. функция выводит данные из файла DataFrame в этом диапазоне"""
    try:
        data_for_filter_by_date = reading_data_from_file('operations.xls')
        data_for_filter_by_date['Дата операции'] = pd.to_datetime(data_for_filter_by_date['Дата операции'],
                                                                format='%d.%m.%Y %H:%M:%S')
        date_obj = datetime.datetime.strptime(user_date, '%Y-%m-%d')
        end_date = pd.to_datetime(user_date)
        start_mounth = date_obj.replace(day=1)
        data_in_interval = data_for_filter_by_date[(data_for_filter_by_date['Дата операции'] >= start_mounth) &
                                    (data_for_filter_by_date['Дата операции'] <= end_date + pd.DateOffset(days=1))]
        logger.info('Успешно. outputting_statistics_based_on_data()')
        return data_in_interval[data_in_interval['Валюта платежа'] == "RUB"]
    except Exception as e:
            logger.error("Произошла ошибка: ", str(e))
            return pd.DataFrame()


def writing_data_to_json(operations: pd.DataFrame) -> list:
    """ преобразование DataFrames в JSON список """
    try:
        json_string = operations.to_json(orient='records', force_ascii=False)
        json_data = json.loads(json_string)
        logger.info("Успешно. writing_data_to_json()")
        return json_data
    except Exception as e:
        logger.error(f"Произошла ошибка при преобразовании DataFrame в JSON: {e}")
        return []
