import json
from random import randint
import pytest
import logging

logger = logging.getLogger("test")


def test_websocket_api_book_instrument_name_depth(crypto_websocket_market_connection, get_book_instrument_case_data):
    """
    Test book.instrument_name.depth websocket API normal case
    Test Data in Config/fixtures/websocket_api_data.yaml
    """
    param_id = get_book_instrument_case_data['param_id']
    method = get_book_instrument_case_data['method']
    channels = get_book_instrument_case_data['channels']
    nonce = get_book_instrument_case_data["nonce"]
    logger.info(f"Starting to test book.instrument_name.depth websocket API, param_id: {param_id}, method: {method}, "
                f"channels: {channels}, nonce: {nonce}")
    crypto_websocket_market_connection.send_info(param_id=param_id, method=method, channels=channels, nonce=nonce)
    status_code, response = crypto_websocket_market_connection.receive()
    logger.info(f"Response status code is {status_code}, response is {response}")
    assert status_code == 101, f"Wesocket API book.instrument_name.depth status code is not 101, it is {status_code}"
    result = response.get("result")
    assert result is not None, f"Response not include key result, response is {response}"
    channel_arr = channels[0].split('.')
    ex_channel, ex_instrument_name,  ex_depth = channel_arr[0], channel_arr[1], int(channel_arr[2])
    assert result['instrument_name'] == ex_instrument_name, f"Instrument name is incorrect"
    assert result["subscription"] == channels[0], "Subscription is incorrect"
    assert result['channel'] == ex_channel, "Channel is incorrect"
    assert result['depth'] == ex_depth, "Depth is incorrect"
    result_data = result['data']
    assert isinstance(result_data, list), "Result Data is not list"
    if len(result_data) > 1:
        for each_data in result_data:
            bids = each_data['bids']
            asks = each_data['asks']
            t = each_data['t']
            assert isinstance(bids, list), "Bids is not list"
            assert isinstance(asks, list), "Asks is not list"
            assert isinstance(t, int), "t is not long type"
            for each_bids in bids:
                price, quantity, order_count = each_bids[0], each_bids[1]. each_bids[2]
                assert isinstance(price, float), "Price type is incorrect"
                assert isinstance(quantity, int), "quantity type is incorrect"
                assert isinstance(order_count, int), "number of orders type is incorrect"
            for each_ask in asks:
                price, quantity, order_count = each_ask[0], each_ask[1].each_ask[2]
                assert isinstance(price, float), "Price type is incorrect"
                assert isinstance(quantity, int), "quantity type is incorrect"
                assert isinstance(order_count, int), "number of orders type is incorrect"


@pytest.mark.parametrize("param_id, method, channels, nonce", [(11, "subscribe", [f"book.ETH_CRO.{randint(0,9)}"], 1587523073344),
                                                               (11, "subscribe", [f"book.ETH_CRO.{randint(11,149)}"], 1587523073344),
                                                               (11, "subscribe", [f"book.ETH_CRO.{randint(151,500)}"], 1587523073344)])
def test_book_instrument_name_depth_api_with_invalid_depth(crypto_websocket_market_connection, param_id, method, channels, nonce):
    """
    Test websocket API book.instrument_name.depth with invalid depth
    return the value depth is always 10 or 150
    """
    logger.info(f"Starting to test book.instrument_name.depth websocket API with invalid depth, param_id: {param_id}, method: {method}, "
                f"channels: {channels}, nonce: {nonce}")
    crypto_websocket_market_connection.send_info(param_id=param_id, method=method, channels=channels, nonce=nonce)
    status_code, response = crypto_websocket_market_connection.receive()
    logger.info(f"Response status code is {status_code}, response is {response}")
    assert status_code == 101, f"Wesocket API book.instrument_name.depth status code is not 101, it is {status_code}"
    result = response.get("result")
    assert result is not None, f"Response not include key result, response is {response}"
    channel_arr = channels[0].split('.')
    ex_channel, ex_instrument_name, ex_depth = channel_arr[0], channel_arr[1], int(channel_arr[2])
    assert result['instrument_name'] == ex_instrument_name, f"Instrument name is incorrect"
    assert result['channel'] == ex_channel, "Channel is incorrect"
    assert result['depth'] == 10 or result['depth'] == 150, "Depth is incorrect"
    result_data = result['data']
    assert isinstance(result_data, list), "Result Data is not list"
    if len(result_data) > 1:
        for each_data in result_data:
            bids = each_data['bids']
            asks = each_data['asks']
            t = each_data['t']
            assert isinstance(bids, list), "Bids is not list"
            assert isinstance(asks, list), "Asks is not list"
            assert isinstance(t, int), "t is not long type"
            for each_bids in bids:
                price, quantity, order_count = each_bids[0], each_bids[1].each_bids[2]
                assert isinstance(price, float), "Price type is incorrect"
                assert isinstance(quantity, int), "quantity type is incorrect"
                assert isinstance(order_count, int), "number of orders type is incorrect"
            for each_ask in asks:
                price, quantity, order_count = each_ask[0], each_ask[1].each_ask[2]
                assert isinstance(price, float), "Price type is incorrect"
                assert isinstance(quantity, int), "quantity type is incorrect"
                assert isinstance(order_count, int), "number of orders type is incorrect"



@pytest.mark.parametrize("param_id, method, channels, nonce", [(None, "subscribe", ["book.ETH_CRO.10"], 1587523073344),
                                                               (11, None, ["book.ETH_CRO.10"], 1587523073344),
                                                               (11, "subscribe", None, 1587523073344),
                                                               (11, "subscribe", ["book.ETH_CRO.150"], None)])
def test_book_instrument_name_depth_api_with_invalid_params(crypto_websocket_market_connection, param_id, method, channels, nonce):
    logger.info(
        f"Starting to test book.instrument_name.depth websocket API with invalid depth, param_id: {param_id}, method: {method}, "
        f"channels: {channels}, nonce: {nonce}")
    crypto_websocket_market_connection.send_info(param_id=param_id, method=method, channels=channels, nonce=nonce)
    status_code, response = crypto_websocket_market_connection.receive()
    logger.info(f"Response status code is {status_code}, response is {response}")
    assert status_code == 101, f"Wesocket API book.instrument_name.depth status code is not 101, it is {status_code}"
    result = response.get("result")
    assert result is not None, f"Response not include key result, response is {response}"
    if channels is not None:
        channel_arr = channels[0].split('.')
        ex_channel, ex_instrument_name, ex_depth = channel_arr[0], channel_arr[1], int(channel_arr[2])















