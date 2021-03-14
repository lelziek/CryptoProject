import pytest
from Utils.config_loader import Configs


def get_candlestick_data():
    get_candlestick_data = Configs.get_fixture_node("common_api_data", "get_candlestick")
    normal_data = get_candlestick_data['normal_data']
    instruments = normal_data['instrument_name']
    timeframe = normal_data['timeframe']
    return_data = []
    for each_instrument in instruments:
        for each_timeframe in timeframe:
            return_data.append((each_instrument, each_timeframe))
    return return_data


@pytest.fixture(scope="session", params=get_candlestick_data(),
                ids=[f"instrument_name: {ins}, testframe: {period}" for ins, period in get_candlestick_data() ])
def get_candlestick_normal_data(request):
    yield request.param


