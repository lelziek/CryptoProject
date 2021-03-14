
CryptoProject
==================

Environment:
--------------

    **Language&Version**: Python 3.8

    **Unit Test Framework**: pytest

    **Tool**: Pycharm Community 2019.3


The CryptoProject framework:
------------------------------------
    **API** - store basic API method

    **Config** - store eenviroment configuration,  enviroment info and test data

    **Fixtures** - store all fixtures, it will used in the test case part

    **Logs** - store logs

    **Test** - Store all test cases

    **Utils** - store all common util method

    **conftest.py**

    **requirement.txt** - store used python library

API Test Cases Location:
----------------------------------
1. *"public/get-candlestick"*:
Test/CommonAPI/test_get_candlestick.py

2. *websocket api "book.{instrument_name}.{depth}"*:
Test/WebsocketAPI/test_websocket_api.py

How to used:
----------------------------------
1.Install python library by command:
 - pip install -r requirement

2.Execute:
 - e.g. (venv) E:\Code\CryptoProject>pytest Tests\CommonAPI\test_get_candlestick.py


