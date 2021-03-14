import pytest
from Utils.config_loader import Configs


def get_book_instrument_data():
    book_instrument_data = Configs.get_fixture_node("websocket_api_data", "book_instrument_name")
    print("instrument_data: ", book_instrument_data)
    return book_instrument_data['normal_case']


@pytest.fixture(scope="session", params=get_book_instrument_data(),
                ids=[f"channels: {item['channels']}" for item in get_book_instrument_data()])
def get_book_instrument_case_data(request):
    yield request.param