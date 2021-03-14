import pytest
from Utils.config_loader import Configs
from API.crypto_common_api import CryptoCommonAPI
from API.websocket_manager import WebsocketManager


@pytest.fixture(scope="session")
def crypto_environment_config():
    crypto_config = Configs.get_environment_node("crypto_config", "automation_main")

    expected_properties = [
        'Environment'
    ]
    for config_property in expected_properties:
        assert crypto_config[config_property] is not None, f'crypto_config.yaml file needs a value for {config_property} before tests can execute. Path: framework\\Config\\environment\\*\\crypto_config.yaml. Node: automation_main'

    return crypto_config


@pytest.fixture(scope="session")
def crypto_environment_info(crypto_environment_config):
    environment_info = Configs.get_environment_node("environment_info", crypto_environment_config['Environment'])

    expected_properties = [
        'api_domain'
    ]
    for config_property in expected_properties:
        assert environment_info[config_property] is not None, f'environment_info.yaml file needs a value for {config_property} before tests can execute. Path: framework\\Config\\environment\\*\\environment_info.yaml. Node: {crypto_environment_config["Environment"]}'

    return environment_info


@pytest.fixture(scope="session")
def crypto_api_domain(crypto_environment_info):
    return crypto_environment_info['api_domain']


@pytest.fixture(scope="session")
def crypto_ws_market_endpoint(crypto_environment_info):
    return crypto_environment_info["ws_market_endpoint"]


@pytest.fixture(scope="module")
def crypto_websocket_market_connection(crypto_ws_market_endpoint):
    ws_market_session = WebsocketManager(crypto_ws_market_endpoint)
    yield ws_market_session
    ws_market_session.close()


@pytest.fixture(scope="session")
def crypto_v2_session(crypto_api_domain):
    crypto_session = CryptoCommonAPI(crypto_api_domain, "v2")
    yield crypto_session


@pytest.fixture(scope="session")
def crypto_v1_session(crypto_api_domain):
    crypto_session = CryptoCommonAPI(crypto_api_domain, "v2")
    yield crypto_session

