import os

import pandas as pd

from src.reports import spending_by_category, write_result_to_file


def test_write_result_to_file():
    data = {'Name': ['John', 'Alice', 'Bob'],
            'Age': [25, 30, 35]}
    df = pd.DataFrame(data)

    filename = 'test_result.txt'

    @write_result_to_file(filename=filename)
    def dummy_function():
        return df

    dummy_function()
    assert os.path.exists(filename), "Файл не найден"

    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()

    expected_content = df.to_string(index=False)
    assert file_content == expected_content, "Содержимое файла не соответствует ожидаемому результату"
    os.remove(filename)


def test_spending_by_category():
    operations = pd.DataFrame({
        'Дата платежа': ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01'],
        'Категория': ['Food', 'Transport', 'Food', 'Shopping'],
        'Сумма': [10, 20, 15, 30]
    })
    filtered_df = spending_by_category(operations, 'Food', '2021-02-01')
    assert len(filtered_df) == 2

    filtered_df = spending_by_category(operations, 'Transport')
    assert len(filtered_df) == 0

    filtered_df = spending_by_category(operations, 'Shopping', '04-01-2021')
    assert len(filtered_df) == 0


@write_result_to_file(filename="test_output.txt")
def multiply_numbers(a, b):
    return a * b
