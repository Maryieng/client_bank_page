from src.views import displaying_statistics_on_cards


def test_displaying_statistics_on_cards():
    json_data = []
    assert displaying_statistics_on_cards(json_data) == displaying_statistics_on_cards(json_data)

    assert displaying_statistics_on_cards('json') == {'Ошибка': "Произошла ошибка:"
                                                                " string indices must be integers, not 'str'"}
