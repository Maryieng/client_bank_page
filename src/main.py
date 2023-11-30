from src.reports import spending_by_category
from src.services import simple_search
from src.utils import (data_currency_and_share_request, outputting_statistics_based_on_data, reading_data_from_file,
                       writing_data_to_json)
from src.views import displaying_statistics_on_cards

data_currency_and_share_request('user_settings.json')
reading_data_from_file('operations.xls')
user_date = input('''Введите дату в формате 'ГГГГ-ММ-ДД'
''')

print(displaying_statistics_on_cards(writing_data_to_json(outputting_statistics_based_on_data(user_date))))

user_decision_to_find_the_value = input("""Воспользоваться поиском операции? Да/Нет
""").lower()
if user_decision_to_find_the_value == 'да':
    user_request = input("""Введите слово/словосочетание для поиска операций:
    """)
    print(simple_search(user_request))

user_decision_by_category = input("""Воспользоваться фильтром по категории? Да/Нет
""").lower()
if user_decision_by_category == 'да':
    user_category = input("""Введите категорию:
    """).title()
    user_category_date = input("""Введите дату в формате 'ГГГГ-ММ-ДД':
    """)
    print(spending_by_category(reading_data_from_file('operations.xls'), user_category, user_category_date))
