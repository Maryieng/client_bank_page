import os
import unittest
from unittest.mock import patch

import pandas as pd
import pytest
import yfinance as yf
from dotenv import load_dotenv
from freezegun import freeze_time

from src.utils import (data_currency_and_share_request, greetings, outputting_statistics_based_on_data,
                       reading_data_from_file, writing_data_to_json)

load_dotenv()


def test_writing_data_to_json():
    data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = pd.DataFrame(data)
    result = writing_data_to_json(df)
    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)
    assert len(result) == df.shape[0]


def test_writing_data_to_json_exception_handling():
    df = pd.DataFrame()
    result = writing_data_to_json(df)
    assert result == []


def test_writing_data_to_json_error():
    assert writing_data_to_json('') == []


@pytest.mark.parametrize("hour, expected_greeting", [
    (6, "Доброе утро!"),
    (14, "Добрый день!"),
    (19, "Добрый вечер!"),
    (2, "Доброй ночи!")
])
@freeze_time("2022-01-01")
def test_greetings(hour, expected_greeting):
    with freeze_time(f"2022-01-01 {hour}:00:00"):
        actual_greeting = greetings()
        assert actual_greeting == expected_greeting


class TestDataReading(unittest.TestCase):
    def test_file_not_found_exception(self):
        filename = "non_existent_file.xlsx"
        with self.assertRaises(FileNotFoundError) as context:
            reading_data_from_file(filename)
        self.assertEqual(str(context.exception), "Файл не найден.")

    def test_exception_handling(self):
        with self.assertRaises(FileNotFoundError) as cm:
            reading_data_from_file("nonexistent_file.xls")
        self.assertEqual(str(cm.exception), "Файл не найден.")


class TestDataOutput(unittest.TestCase):
    def test_empty_data_frame(self):
        pd.DataFrame()
        result = outputting_statistics_based_on_data('2022-01-03')
        self.assertTrue(result.empty)


class TestDataCurrencyAndShareRequest(unittest.TestCase):
    def test_file_not_found_error(self):
        filename = "nonexistent_file.json"
        exchange_rates, share_prices = data_currency_and_share_request(filename)

        self.assertEqual(exchange_rates, [])
        self.assertEqual(share_prices, [])

    def test_api_request_error(self):
        filename = "your_file.json"
        os.environ['api_key_openexchangerates'] = "invalid_api_key"
        exchange_rates, share_prices = data_currency_and_share_request(filename)

        self.assertEqual(exchange_rates, [])
        self.assertEqual(share_prices, [])

    @patch('builtins.open')
    @patch('os.path')
    def test_file_not_found(self, mock_os_path, mock_open):
        mock_os_path.dirname.return_value = 'dummy_directory'
        mock_os_path.join.return_value = 'dummy_file_path'
        mock_open.side_effect = FileNotFoundError
        result = data_currency_and_share_request('dummy_filename')
        self.assertEqual(result, ([], []))


def test_data_currency_and_share_request_error_read():
    assert data_currency_and_share_request('dd') == ([], [])


def get_share_prices(text):
    share_prices = []

    for stock in text['user_stocks']:
        symbol = yf.Ticker(stock)
        stock_info = symbol.info

        if "currentPrice" in stock_info:
            current_price = stock_info["currentPrice"]
            share_prices.append({"Акция": stock, "Цена": current_price})

    return share_prices


class SharePriceTests(unittest.TestCase):
    def test_share_prices_empty_when_no_current_price(self):
        text = {'user_stocks': ['AAPL', 'GOOG']}
        expected_share_prices = []

        with patch.object(yf.Ticker, 'info') as mock_info:
            mock_info.return_value = {}
            share_prices = get_share_prices(text)

        self.assertEqual(share_prices, expected_share_prices)
