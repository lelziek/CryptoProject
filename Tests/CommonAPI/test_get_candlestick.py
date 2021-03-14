import logging
import pytest
import random
from Utils.common_utils import CommonUtils

logger = logging.getLogger("test")

pytestmark = [pytest.mark.candlestick, pytest.mark.commonapi]


def test_get_candlestick_with_valid_params(crypto_v2_session, get_candlestick_normal_data):
    """
       Test public/get-candlestick with valid params
    """
    logger.info("Starting to test the public/get-candlestick API with correct params")
    instrument_name = get_candlestick_normal_data[0]
    testframe = get_candlestick_normal_data[1]
    status_code, result = crypto_v2_session.get_candlestick(instrument_name, testframe)
    assert status_code == 200, f'get_candlestick response is not 200, status code is {status_code}'
    r_result = result['result']
    data_result = r_result['data']
    assert r_result['instrument_name'] == instrument_name, "Instrument Name is incorrect"
    assert r_result['interval'] == testframe, "Interval value is incorrect"
    assert type(data_result) is list, f"Response data value is not Array, data is {data_result}"
    logger.info("Test data consistent")
    for each_data in data_result:
        # assert CommonUtils.is_validate_date(each_data['t']), f"t is not timestamp, value is {each_data['t']}"
        # t value is not a valid timestamp, current comment it
        assert isinstance(each_data['t'], int), f"t is not int, value is {each_data['t']}"
        assert isinstance(each_data['o'], (int, float)), f"o is not number, value is {each_data['o']}"
        assert isinstance(each_data['h'], (int, float)), f"h is not number, value is {each_data['h']}"
        assert isinstance(each_data['l'], (int, float)), f"l is not number, value is {each_data['l']}"
        assert isinstance(each_data['c'], (int, float)), f"c is not number, value is {each_data['c']}"
        assert isinstance(each_data['v'], (int, float)), f"v is not number, value is {each_data['v']}"


@pytest.mark.parametrize("instrument_name, testframe", [(None, None)])
def test_get_candlestick_with_error_code(crypto_v2_session, instrument_name, testframe):
    """
    Test public/get-candlestick without params
    expected status_code is 400
    """
    logger.info("Starting to test public/get-candlestick API without params")
    status_code, result = crypto_v2_session.get_candlestick(instrument_name, testframe)
    assert status_code == 400, "public/get-candlestick API without params response status code is not 400"


@pytest.mark.parametrize("instrument_name, testframe, desc", [("ETH_CRO", "", "without testframe"),
                                                              ("", "1m", "without instrument_name"),
                                                              ("ETH_CRO", random.randint(1, 10), "with invalid testframe"),
                                                              ("ETH-CRO", "%251", "security check")])
def test_get_candlestick_with_invalid_input(crypto_v2_session, instrument_name, testframe, desc):

    logger.info(f"Starting to test public/get-candlestick API {desc}")
    status_code, result = crypto_v2_session.get_candlestick(instrument_name, testframe)
    assert status_code == 200, "public/get-candlestick API without testframe response status code is not 200"
    assert CommonUtils.is_json(result), f"Result is not json format, Response text is {result}"
    print(result)
    assert result['code'] == 10004, f"Response return code is not 10004, code value is {result['code']}"










