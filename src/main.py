from src.services import simple_search
from src.views import displaying_statistics_on_cards
from src.utils import outputting_statistics_based_on_data, data_currency_and_share_request, reading_data_from_file, \
    writing_data_to_json

data_currency_and_share_request('user_settings.json')
reading_data_from_file('operations.xls')
user_date = input(f'''Введите дату в формате 'ГГГГ-ММ-ДД'
''')

print(displaying_statistics_on_cards(writing_data_to_json(outputting_statistics_based_on_data(user_date))))

user_request = input("""Введите слово/словосочетание для поиска операций:
""")
print(simple_search(user_request))
